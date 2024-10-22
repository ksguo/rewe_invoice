from fastapi import APIRouter, status, Depends
import os
from typing import List
from app.db.models import (
    User,
    Purchase,
    SupermarketChain,
    SupermarketBranch,
    PaymentMethod,
    PurchasedProduct,
)
from app.user_management.router import get_current_active_user
from app.db.database import get_db
from app.ocr_service.ocr_pdf import scan_invoice
from app.ocr_service.invoice_process_pdf import extract_invoice_data
from datetime import datetime
from app.db.crud import update_record
from app.ocr_service.ocr_image import detect_text, clean_and_classify_text
import logging

router = APIRouter()


@router.post(
    "/process-invoices-pdf",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Tesseract OCR:Recognize text and extract data from multiple invoice files",
    description="Performs text recognition on multiple uploaded files and extracts invoice data from each.",
    tags=["invoice_processing"],
    responses={
        200: {"description": "Data extracted successfully"},
        404: {"description": "One or more files not found"},
        403: {"description": "Unauthorized access to file"},
    },
)
async def process_invoices(
    purchase_ids: List[int], current_user: User = Depends(get_current_active_user)
):
    results = {}
    with get_db() as db:
        for purchase_id in purchase_ids:
            purchase = (
                db.query(Purchase)
                .filter(
                    Purchase.purchase_id == purchase_id,
                    Purchase.user_id == current_user.user_id,
                )
                .first()
            )
            if not purchase:
                results[str(purchase_id)] = "Unauthorized access or file does not exist"
                continue
            if not os.path.exists(purchase.file_path):
                results[purchase.file_name] = "File not found"
                continue
            recognized_text = scan_invoice(purchase.file_path)
            with open(f"{purchase.file_path}.txt", "w") as text_file:
                text_file.write("\n".join(recognized_text))
            extracted_data = extract_invoice_data(recognized_text)

            # Fetch or create the supermarket chain
            chain = (
                db.query(SupermarketChain)
                .filter_by(chain_name=extracted_data["brand"])
                .first()
            )
            if not chain:
                chain = SupermarketChain(chain_name=extracted_data["brand"])
                db.add(chain)
                db.commit()
                db.refresh(chain)

            # fetch or create the supermarket branch
            branch = (
                db.query(SupermarketBranch)
                .filter_by(branch_chaininternal_id=extracted_data["markt_id"])
                .first()
            )
            if not branch:
                branch = SupermarketBranch(
                    chain_id=chain.chain_id,
                    branch_name=extracted_data["markt_name"],
                    branch_chaininternal_id=extracted_data["markt_id"],
                    branch_street=extracted_data["store_address"].split(",")[0],
                    branch_plz=extracted_data["store_address"].split()[-2],
                    branch_ort=extracted_data["store_address"].split()[-1],
                    branch_tel=extracted_data["telephone"],
                    branch_uid_number=extracted_data["uid_number"],
                    branch_created=datetime.now(),
                )
                db.add(branch)
                db.commit()
                db.refresh(branch)

            # fetch or create payment method
            payment_method = (
                db.query(PaymentMethod)
                .filter_by(paymentmethod_name=extracted_data["payment_method"])
                .first()
            )
            if not payment_method:
                payment_method = PaymentMethod(
                    paymentmethod_name=extracted_data["payment_method"]
                )
                db.add(payment_method)
                db.commit()
                db.refresh(payment_method)

            update_record(
                db,
                Purchase,
                purchase_id,
                purchase_sum=float(extracted_data["total"].replace(",", ".")),
                purchase_time=datetime.strptime(
                    f"{extracted_data['date']} {extracted_data['time']}",
                    "%d.%m.%Y %H:%M",
                ),
                paymentmethod_id=payment_method.paymentmethod_id,
                branch_id=branch.branch_id,
                purchase_processed=datetime.now(),
                receipt_nr=extracted_data.get("receipt_nr"),
                document_nr=extracted_data.get("document_nr"),
                trace_nr=extracted_data.get("trace_nr"),
                purchase_used_discount_type=extracted_data.get("discount_used_payback"),
                cashier_number=extracted_data["cashier_number"],
                register_number=extracted_data["register_number"],
            )
            db.commit()

            # insert purchased products
            for item in extracted_data["items"]:
                purchased_product = PurchasedProduct(
                    purchase_id=purchase_id,
                    purchased_product_name=item["description"],
                    purchased_product_price=float(item["unit_price"].replace(",", ".")),
                    purchased_product_qty=item["quantity"],
                )
                db.add(purchased_product)
            db.commit()

            results[purchase.file_name] = extracted_data

    return results


@router.post(
    "/process-invoice-images",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Google Cloud Vesion OCR :use Recognize text and extract data from image files linked to purchases",
    description="Performs text recognition on image files linked to purchase records and "
    "extracts data, updating the database accordingly.",
    tags=["invoice_processing"],
    responses={
        200: {"description": "Data processed successfully"},
        404: {"description": "File not found or unauthorized access"},
        403: {"description": "Unauthorized access to file"},
        500: {"description": "Internal Server Error"},
    },
)
async def process_images(
    purchase_ids: List[int], current_user: User = Depends(get_current_active_user)
):
    results = {}
    with get_db() as db:
        for purchase_id in purchase_ids:
            purchase = (
                db.query(Purchase)
                .filter(
                    Purchase.purchase_id == purchase_id,
                    Purchase.user_id == current_user.user_id,
                )
                .first()
            )
            if not purchase:
                results[str(purchase_id)] = "Unauthorized access or file does not exist"
                continue
            if not os.path.exists(
                purchase.file_path
            ) or not purchase.file_path.endswith(("jpg", "jpeg", "png")):
                results[purchase.file_name] = "Image file not found"
                continue

            detected_text = detect_text(purchase.file_path)
            if detected_text:
                structured_data = clean_and_classify_text(detected_text)
                if structured_data:
                    try:
                        # Check for all required fields
                        required_fields = [
                            "brand",
                            "markt_id",
                            "markt_name",
                            "store_address",
                            "telephone",
                            "uid_number",
                        ]
                        if any(
                            field not in structured_data for field in required_fields
                        ):
                            raise ValueError(
                                f"Missing fields in structured data: {required_fields}"
                            )

                        # Update Supermarket Chain
                        chain = (
                            db.query(SupermarketChain)
                            .filter_by(chain_name=structured_data["brand"])
                            .first()
                        )
                        if not chain:
                            chain = SupermarketChain(
                                chain_name=structured_data["brand"]
                            )
                            db.add(chain)
                            db.commit()
                            db.refresh(chain)

                        # Update Supermarket Branch
                        branch = (
                            db.query(SupermarketBranch)
                            .filter_by(
                                branch_chaininternal_id=structured_data["markt_id"]
                            )
                            .first()
                        )
                        if not branch:
                            branch = SupermarketBranch(
                                chain_id=chain.chain_id,
                                branch_name=structured_data["markt_name"],
                                branch_chaininternal_id=structured_data["markt_id"],
                                branch_street=structured_data["store_address"].split(
                                    ","
                                )[0],
                                branch_plz=structured_data["store_address"].split()[-2],
                                branch_ort=structured_data["store_address"].split()[-1],
                                branch_tel=structured_data["telephone"],
                                branch_uid_number=structured_data["uid_number"],
                                branch_created=datetime.now(),
                            )
                            db.add(branch)
                            db.commit()
                            db.refresh(branch)

                        # Update Payment Method
                        payment_method = (
                            db.query(PaymentMethod)
                            .filter_by(
                                paymentmethod_name=structured_data["payment_method"]
                            )
                            .first()
                        )
                        if not payment_method:
                            payment_method = PaymentMethod(
                                paymentmethod_name=structured_data["payment_method"]
                            )
                            db.add(payment_method)
                            db.commit()
                            db.refresh(payment_method)

                        # Update Purchase
                        purchase_time = datetime.strptime(
                            f"{structured_data['date']} {structured_data['time']}",
                            "%d.%m.%Y %H:%M:%S",
                        )
                        update_record(
                            db,
                            Purchase,
                            purchase_id,
                            purchase_sum=float(
                                structured_data["total"].replace(",", ".")
                            ),
                            purchase_time=purchase_time,
                            paymentmethod_id=payment_method.paymentmethod_id,
                            branch_id=branch.branch_id,
                            purchase_processed=datetime.now(),
                            receipt_nr=structured_data.get("receipt_nr"),
                            document_nr=structured_data.get("document_nr"),
                            trace_nr=structured_data.get("trace_nr"),
                            purchase_used_discount_type=structured_data.get(
                                "discount_used_payback"
                            ),
                            cashier_number=structured_data["cashier_number"],
                            register_number=structured_data["register_number"],
                        )
                        db.commit()

                        # Insert Purchased Products
                        for item in structured_data["items"]:
                            purchased_product = PurchasedProduct(
                                purchase_id=purchase_id,
                                purchased_product_name=item["description"],
                                purchased_product_price=float(
                                    item["unit_price"].replace(",", ".")
                                ),
                                purchased_product_qty=item["quantity"],
                            )
                            db.add(purchased_product)
                        db.commit()

                        results[purchase.file_name] = structured_data
                    except Exception as e:
                        logging.error(
                            f"Error processing image data for purchase {purchase_id}: {e}"
                        )
                        results[purchase.file_name] = "Error processing data"
                else:
                    results[purchase.file_name] = "Failed to process data"
            else:
                results[purchase.file_name] = "No text detected in image"

    return results
