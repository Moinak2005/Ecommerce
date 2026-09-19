import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
from google import genai
from google.genai import types
from django.conf import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def search_catalog(keywords: str, max_price: float = None) -> str:
    """
    Search available products in the store by keyword and optional maximum price.
    """
    return '{"status": "found", "items": [{"id": 1, "name": "Red Dress", "price": 100.0}]}'

def add_to_cart(product_ids: list[int]) -> str:
    """
    Add a list of product IDs to the user's cart.
    """
    print(f"TOOL CALLED: add_to_cart({product_ids})")
    return f"Successfully added to cart: {product_ids}"

chat = client.chats.create(
    model='gemini-flash-lite-latest',
    config=types.GenerateContentConfig(
        tools=[search_catalog, add_to_cart],
        temperature=0.7,
    )
)
print("Sending message...")
response = chat.send_message("I want to buy a red dress. Add it to my cart.")
print("Response:", response.text)
