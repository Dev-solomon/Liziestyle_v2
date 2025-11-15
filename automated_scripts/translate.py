from product_model import Product #get the product model
from openai import OpenAI
import os
from pymongo import UpdateOne, bulk


def translate_to_italian(text):
    # Read API key from environment variables
    api_key = os.getenv('OPENAI_KEY')
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use "gpt-3.5-turbo" for a cheaper alternative
        messages=[
            {"role": "system", "content": "You are a translator."},
            {"role": "user", "content": f"only give the Translation of {text} in English:"}
        ]
    )
    return response.choices[0].message.content



def retrieve():
    """Retrieve products from the database."""
    try:
        products = list(Product.collection.find().limit(129).skip(0))
        return products  # Return the retrieved products
    except Exception as e:
        print(f"Error retrieving products: {e}")
        
        return []
    
    
bulk_operations = []

try:
    a = retrieve() 
    if a != []:
        for b in a:
            update_query = {
                "$set": {
                    "title": translate_to_italian(b["title"]),
                    "description": translate_to_italian(b["description"]),
                    "category": translate_to_italian(b["category"]),
                    "tags": [translate_to_italian(tag) for tag in b["tags"]],
                }
            }
            bulk_operations.append(UpdateOne({"_id": b["_id"]}, update_query))

        if bulk_operations:
            # print(bulk_operations)
            result = Product.collection.bulk_write(bulk_operations)
            print(f"Successfully updated {result.modified_count} products.")
    else:
        print("No products to insert.")
except Exception as e:
    print(f"Error inserting products: {e}")
    
