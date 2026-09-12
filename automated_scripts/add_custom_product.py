import requests # request module
import json #json module
from bson import ObjectId #objectid module
from termcolor import colored #for colors on the console
import re #regex filtering
import os
import datetime #datetime
import time #time
import string #string
import random #random module
from product_model import Product #get the product model
from pymongo import MongoClient, errors #mongodb
from openai import OpenAI

# AI function to create description for a product
def write_description(title, image_link):
    # Read API key from environment variables
    api_key = os.getenv('OPENAI_KEY') 
    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"write 50 words for description of my product for customers to buy, here is the {title} and the link to the image here{image_link}. Don't repeat words and stop using elevate, also do not add the link to the image in description. make the different descriptions unique and catchy to the customer. Do not surround the title with quotes"
            }
        ]
    )

    # print(completion.choices[0].message["content"])
    return completion.choices[0].message.content

# create array of tags
def create_tags_list(input_string):
    # Strip extra spaces
    input_string = input_string.strip()

    # If empty input, return empty list
    if not input_string:
        return []

    # Split by commas and remove extra spaces
    tags = [tag.strip() for tag in input_string.split(',') if tag.strip()]

    return tags

def create_image_list(input_string):
    # Strip extra spaces
    input_string = input_string.strip()

    # If empty, return empty list
    if not input_string:
        return []

    # Split by commas and clean each URL
    images = [img.strip() for img in input_string.split(',') if img.strip()]

    return images

def create_variants_list(input_string):
    # Strip extra spaces
    input_string = input_string.strip()

    # If empty, return empty list
    if not input_string:
        return []

    # Split by commas and clean each URL
    variants_list = [[variant.strip(), "Standard Customized LIZIES"] for variant in  input_string.split(',')]

    return variants_list

catalog = [] # this is the catalog for storing a new product

def create_new_custom_product():
    # Generate a string for the id
    length = 24   # Define the length of the random string
    # Create a pool of characters (small alphabets and digits)
    characters = string.ascii_lowercase + string.digits
    generated_ID = ''.join(random.choice(characters) for _ in range(length))

    # title for custom product
    product_title = str(input("Enter Product Title: ")).strip()
    # Enter Images link for custom product
    product_images = create_image_list(input("Enter image URLs separated by commas: "))
    # Enter the Price in Euro
    product_price = float(input("What is the sale price?: "))
    # Make a product description from func
    product_description = write_description(product_title, product_images[0])
    # the product category
    product_category = input("Enter Product Category: ")
    # tags for the product
    product_tags = create_tags_list(input("Enter tags separated by commas: "))
    sales_offer = 0 # sales-offer
    # stock available for single product
    stock = int(input("Enter Stock Count Available: "))
    # Enter variants list
    variants = create_variants_list(input("Enter variants separated by commas(,): "))
    weight = 0.6 # weight in kg for the product 
    featured = "false" # product has not been featured
    units = 1 # a single unit being sold
    video = str(input("Enter Video Link: ")).strip() # is there a video for the product?
    createdAt =  datetime.datetime.now() # time the product was created.


    print(colored(f'READY TO INSERT NEW PRODUCT, CONFRIM YES OR NO!', 'yellow'))
    confirmation = str(input("Continue With Process: ")).strip()

    try:
        if confirmation.upper() == "YES":
            # Attempt to insert new document
            new_custom_product = Product.collection.insert_one(
                {
                        "_id": generated_ID,
                        "user": ObjectId('676716d67602c42f64f06f94'),
                        "title": product_title,
                        "images": product_images,
                        "price": product_price,
                        "description": product_description,
                        "category": "customs", #category in database
                        "tags": product_tags,
                        "salesOffer": sales_offer,
                        "stock": stock,
                        "variants": variants,
                        "weight": weight,
                        "featured": featured,
                        "units": units,
                        "video": video,
                        "createdAt": createdAt
                }
            )

            # Check if any products were successfully inserted
            if new_custom_product.inserted_id:
                return colored(f"Successfully inserted product with ID: {new_custom_product.inserted_id}", 'cyan')
            else:
                return colored("Insert failed. No product was inserted.", 'red')
    
    except Exception as e:
         print(colored(f"Database Error:=>  {e}", "red"))


# CALL THE FUNCTION TO RUN SCRIPT
create_new_custom_product()