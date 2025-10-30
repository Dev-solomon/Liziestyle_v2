from openai import OpenAI
import os



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
                "content": f"write 50 words for description of my product for customers to buy, here is the {title} and the link to the image here{image_link}. Don't repeat words and stop using elevate, also do not add the link to the image in description. make the different descriptions unique and catchy to the customer."
            }
        ]
    )

    # print(completion.choices[0].message["content"])
    return completion.choices[0].message.content

# print(write_description("Winter Knitted Plush Floor Socks Home Warm Non-slip Carpet Socks Women", "https://cf.cjdropshipping.com/5e3cec90-422c-44c9-8606-d67332ad34f8.jpg"))
    


def translate_to_italian(text):
    # Read API key from environment variables
    api_key = os.getenv('OPENAI_KEY')
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use "gpt-3.5-turbo" for a cheaper alternative
        messages=[
            {"role": "system", "content": "You are a translator."},
            {"role": "user", "content": f"only give the Translation of {text} in Italian:"}
        ]
    )
    return response.choices[0].message.content

# # Example usage
english_text = ["Hello", "How are you?", "Good morning", "Welcome"]
italian_translation = [translate_to_italian(a) for a in english_text]
print(italian_translation)
