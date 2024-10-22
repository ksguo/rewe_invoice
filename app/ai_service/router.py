from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.db.models import (
    User,
    Purchase,
    PurchasedProduct,
    SupermarketBranch,
    PaymentMethod,
    UserAnalysis,
)
from app.user_management.router import get_current_active_user
from openai import OpenAI
from dotenv import load_dotenv
import os
from enum import Enum
from typing import List
from pydantic import BaseModel
from datetime import datetime


router = APIRouter()

"""
####################################################
get user all invoice data
####################################################
"""


def get_user_data(user_id: int, db: Session):
    purchases = db.query(Purchase).filter(Purchase.user_id == user_id).all()
    results = []
    for purchase in purchases:
        products = (
            db.query(PurchasedProduct)
            .filter(PurchasedProduct.purchase_id == purchase.purchase_id)
            .all()
        )
        product_details = [
            {
                "product_name": product.purchased_product_name,
                "product_price": product.purchased_product_price,
                "quantity": product.purchased_product_qty,
            }
            for product in products
        ]

        branch = (
            db.query(SupermarketBranch)
            .filter(SupermarketBranch.branch_id == purchase.branch_id)
            .first()
        )
        payment_method = (
            db.query(PaymentMethod)
            .filter(PaymentMethod.paymentmethod_id == purchase.paymentmethod_id)
            .first()
        )

        results.append(
            {
                "purchase_id": purchase.purchase_id,
                "branch": {
                    "name": branch.branch_name if branch else "Unknown",
                    "street": branch.branch_street,
                    "postal_code": branch.branch_plz,
                    "city": branch.branch_ort,
                    "telephone": branch.branch_tel,
                    "uid_number": branch.branch_uid_number,
                },
                "payment_method": (
                    payment_method.paymentmethod_name if payment_method else "Unknown"
                ),
                "total_amount": purchase.purchase_sum,
                "purchase_time": purchase.purchase_time.isoformat(),
                "receipt_nr": purchase.receipt_nr,
                "document_nr": purchase.document_nr,
                "trace_nr": purchase.trace_nr,
                "register_number": purchase.register_number,
                "cashier_number": purchase.cashier_number,
                "discount_used": purchase.purchase_used_discount_type,
                "products": product_details,
            }
        )

    return results


@router.get(
    "/user/{user_id}/all-data",
    response_model=list,  # Assuming the response is a list of user purchase data
    status_code=status.HTTP_200_OK,
    summary="Fetch all purchase data for a specific user",
    description="Retrieves all purchase records linked to a specific user, including detailed"
    "information about each purchase.",
    tags=["ai_service"],
    responses={
        200: {
            "description": "Data retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "purchase_id": 1,
                        "branch": "Branch Details",
                        "products": ["Product Details"],
                    }
                }
            },
        },
        403: {
            "description": "Unauthorized access to user data",
            "content": {
                "application/json": {
                    "example": {"detail": "Unauthorized to access this user's data"}
                }
            },
        },
        404: {
            "description": "User data not found",
            "content": {
                "application/json": {
                    "example": {"detail": "No data found for this user"}
                }
            },
        },
    },
)
def fetch_all_user_data(
    user_id: int, current_user: User = Depends(get_current_active_user)
):
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=403, detail="Unauthorized to access this user's data."
        )

    with get_db() as db:
        return get_user_data(user_id, db)


"""
####################################################
chatgpt part
####################################################
"""


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY", "")
client = OpenAI(api_key=openai_api_key)


class AnalysisCategory(str, Enum):
    EatingHabits = "Eating Habits"
    LifestyleHobbies = "Lifestyle and Hobbies"
    MaritalStatus = "Marital Status and Household"
    FinancialStatus = "Financial Status"
    EthnicBackground = "Ethnic and Cultural Background"
    TimeManagement = "Time Management and Daily Structure"
    PersonalValues = "Personal Preferences and Values"


def create_chatgpt_prompt(user_data, categories: List[str]):
    prompt = "Analyze the following detailed purchase data for the user and "
    "provide insights based on the selected categories:\n"
    for category in categories:
        prompt += f"- {category}\n"

    prompt += "\nDetailed purchase data includes:\n"
    for item in user_data:
        prompt += (
            f"Purchase ID {item['purchase_id']} at {item['branch']['name']} "
            f"({item['branch']['city']}), on {item['purchase_time']}, totaling ${item['total_amount']}:\n"
            f"  - Store Details: {item['branch']['street']}, {item['branch']['postal_code']} "
            f"{item['branch']['city']}, Tel: {item['branch']['telephone']}, UID: {item['branch']['uid_number']}\n"
            f"  - Payment Method: {item['payment_method']}\n"
            "  - Products Purchased:\n"
        )
        for product in item["products"]:
            prompt += (
                f"    - {product['product_name']}: ${product['product_price']} each, "
                f"Quantity: {product['quantity']}\n"
            )
        prompt += (
            f"  - Receipt No: {item['receipt_nr']}, Document No: {item['document_nr']}, "
            f"Trace No: {item['trace_nr']}\n"
            f"  - Register No: {item['register_number']}, Cashier No: {item['cashier_number']}\n"
        )
        if item["discount_used"]:
            prompt += f"  - Discount Used: {item['discount_used']}\n"
        prompt += "\n"

    prompt += "Please provide detailed insights that can help understand "
    "the user's preferences and habits related to the selected categories based on the data provided above."
    return prompt


def save_insights(db, user_id: int, insights: str, analysis_type: str):
    new_analysis = UserAnalysis(
        user_id=user_id,
        analysis_type=analysis_type,
        insights=insights,
        analysis_date=func.now(),
    )
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)
    return new_analysis


@router.post(
    "/analyze-user/{user_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Analyzes user purchases and provides AI-driven insights based on selected categories",
    description="Uses OpenAI's GPT to analyze purchase data linked to the user "
    "based on selected categories and provides insights.",
    tags=["ai_service"],
    responses={
        200: {"description": "Insights generated and stored successfully"},
        403: {"description": "Unauthorized access to user data"},
        404: {"description": "User not found"},
        500: {"description": "Error processing the request"},
    },
)
async def analyze_user_data(
    user_id: int,
    categories: List[str] = Query([e.value for e in AnalysisCategory]),
    current_user: User = Depends(get_current_active_user),
):
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=403, detail="Unauthorized to access this user's data."
        )

    with get_db() as db:
        user_data = get_user_data(user_id, db)
        if not user_data:
            raise HTTPException(status_code=404, detail="No data found for this user.")

        prompt = create_chatgpt_prompt(user_data, categories)
        analysis_type = ", ".join(categories)  # 创建一个字符串来描述分析类型
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
            )
            insights = completion.choices[0].message.content.strip()
            saved_analysis = save_insights(db, user_id, insights, analysis_type)
            return {
                "response": "Insights generated and stored successfully",
                "analysis_id": saved_analysis.analysis_id,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


"""
####################################################
get user analysis data
####################################################
"""


class UserAnalysisResponse(BaseModel):
    analysis_id: int
    user_id: int
    analysis_type: str
    insights: str
    analysis_date: datetime


@router.get(
    "/user/{user_id}/analyses",
    response_model=List[UserAnalysisResponse],
    status_code=status.HTTP_200_OK,
    summary="Retrieve all analyses for a specific user",
    description="Fetches all the analysis records associated with a specific user.",
    tags=["ai_service"],
    responses={
        200: {"description": "Analyses retrieved successfully"},
        404: {"description": "User not found or no analysis data available"},
        403: {"description": "Unauthorized access to user data"},
    },
)
def get_user_analyses(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=403, detail="Unauthorized to access this user's data."
        )

    with db as session:
        user_analyses = (
            session.query(UserAnalysis).filter(UserAnalysis.user_id == user_id).all()
        )
        if not user_analyses:
            raise HTTPException(
                status_code=404, detail="No analysis data found for this user."
            )
        return user_analyses
