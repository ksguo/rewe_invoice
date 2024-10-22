import os
import json
from google.cloud import vision
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import HTTPException


load_dotenv()

# google cloud service
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS", ""
)
# openai service
openai_api_key = os.getenv("OPENAI_API_KEY", "")
client = OpenAI(api_key=openai_api_key)


def detect_text(path: str):
    """user Google Vision API recoginzie text of invoice image。"""
    client_vision = vision.ImageAnnotatorClient()
    try:
        with open(path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)
        response = client_vision.text_detection(image=image)
        if response.error.message:
            raise HTTPException(status_code=500, detail=str(response.error.message))

        return (
            response.text_annotations[0].description
            if response.text_annotations
            else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def clean_and_classify_text(text):
    """uses ChatGPT to clean, classify, and structure text into a defined JSON format for an invoice."""
    try:
        prompt = f"""
        Analyze the following receipt text and extract information to fill in the JSON structure.
        The expected categories are:
        - Market name
        - Store address
        - Telephone number
        - UID number (tax identification number)
        - Items, each with a description, total price, quantity, and unit price
        - Total amount paid
        - Date of transaction
        - Time of transaction
        - Payment method
        - Receipt number (Bon-Nr.)
        - Document number (Beleg-Nr.)
        - Trace number (Seriennnummer Kasse)
        - Brand (default to REWE)
        - Market ID
        - Register number
        - Cashier number
        - Discount used (e.g., PAYBACK card number)

        Based on this template, structure the receipt information:

        Text: {text}

        Example of expected output format:
        {{
            "markt_name": "REWE MARKT GmbH",
            "store_address": "Luxemburger Str. 150, 50937 Köln",
            "telephone": "0221-94081691",
            "uid_number": "DE812706034",
            "items": [
                {{"description": "BUTTER BRIOCHE", "total_price": "2,89", "quantity": 1, "unit_price": "2,89"}},
                {{"description": "CHERRYROMATOMATE", "total_price": "1,98", "quantity": 2, "unit_price": "0,99"}},
                {{"description": "SCH.SCH ZERO", "total_price": "2,64", "quantity": 3, "unit_price": "0,88"}},
                {{"description": "TOPFREINIGER", "total_price": "0,75", "quantity": 1, "unit_price": "0,75"}}
            ],
            "total": "9,01",
            "date": "28.05.2024",
            "time": "19:40",
            "payment_method": "Mastercard",
            "receipt_nr": "525",
            "document_nr": "3225",
            "trace_nr": "769518",
            "brand": "REWE",
            "markt_id": "0014",
            "register_number": "2",
            "cashier_number": "151515",
            "discount_used_payback": "PAYBACK#########5975"
        }}
        """
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Adjust to the correct model as necessary
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": "Please format the above text into the specified JSON structure.",
                },
            ],
        )
        # correctly accessing the content of the completion message
        structured_response = completion.choices[0].message.content
        # parse and return as dictionary
        return json.loads(structured_response)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
