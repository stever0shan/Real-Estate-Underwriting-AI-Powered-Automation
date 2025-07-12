import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_custom_prompt(field_name):
    prompts = {
        "monthly_rent": "What is the monthly rent for the property?",
        "NOI": "What is the Net Operating Income (NOI) in dollars?",
        "cap_rate": "What is the capitalization rate for the property?",
        "total_units": "How many total units or apartments are there?",
        "purchase_price": "What is the purchase price or sale price of the property?",
        "loan_amount": "What is the loan amount or construction financing amount?",
        "developer_equity": "What is the developer's equity contribution or sponsor equity?"
    }
    return prompts.get(field_name, f"What is the value for: {field_name}?")

def ai_fill_field(parsed_text, field_name):
    prompt = f"""
Given this Offering Memorandum text:

--- BEGIN TEXT ---
{parsed_text}
--- END TEXT ---

{get_custom_prompt(field_name)}

If you cannot find it, return 'NEEDS_REVIEW'.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f" GPT error on field '{field_name}': {e}")
        return "NEEDS_REVIEW"

def ai_fill_fields(parsed_text, missing_fields):
    result = {}
    for field in missing_fields:
        result[field] = ai_fill_field(parsed_text, field)
    return result
