from google import genai
from google.genai import types
from django.conf import settings
from myapp.models import Product
import json

# Assuming GEMINI_API_KEY is defined in settings.py
# If not, the user will need to add it: GEMINI_API_KEY = "your_api_key_here"
client = genai.Client(api_key=getattr(settings, 'GEMINI_API_KEY', 'DUMMY_KEY'))

def search_catalog(keywords: str, max_price: float = None) -> str:
    """
    Search available products in the store by keyword and optional maximum price.
    """
    qs = Product.objects.filter(is_active=True)
    
    if max_price:
        qs = qs.filter(price__lte=max_price)

    # Search in name or description
    matched = qs.filter(name__icontains=keywords) | qs.filter(description__icontains=keywords)
    matched = matched.distinct()[:6]

    if not matched.exists():
        return json.dumps({"status": "no_results", "items": []})

    results = []
    for item in matched:
        results.append({
            "id": item.id,
            "name": item.name,
            "price": float(item.discount_price if item.discount_price else item.price),
            "description": item.description[:120] if item.description else ""
        })
    return json.dumps({"status": "found", "items": results})

def get_ai_stylist_recommendation(user_prompt: str, user=None, chat_history: list = None) -> dict:
    """
    Processes user request, allows Gemini to query the catalog via tools,
    and returns a structured styling proposal.
    """
    system_instruction = """
    You are a friendly and expert assistant for an Organic Grocery Store.
    Your goal is to help customers find fresh organic produce, groceries, and ingredients for their recipes, while staying within their budget.
    
    Rules:
    1. ALWAYS call `search_catalog` to inspect what items actually exist in our organic inventory.
    2. NEVER invent fake product IDs or products that aren't returned by `search_catalog`.
    3. Stay strictly within the user's budget if one is stated.
    4. Keep your commentary helpful, concise, and enthusiastic about healthy eating.
    5. If the user tells you they want to buy a product, use the `add_to_cart` tool to add it to their cart.
    6. ALWAYS quote prices and currency in Indian Rupees (₹), never in dollars.
    7. CRITICAL: When recommending products or asking if the user wants to add them to their cart, you MUST include the product IDs in your text (e.g. "Paneer (ID: 12)") so you don't forget the ID when the user replies "yes".
    """

    def add_to_cart(product_ids: list[int]) -> str:
        """
        Add a list of product IDs to the user's cart.
        Call this when the user says they want to buy a product.
        """
        if not user or not user.is_authenticated:
            return "Error: Tell the user they must log in to add items to their cart."
        
        from myapp.models import Order, OrderItem, Product
        from django.db import transaction
        
        added = []
        try:
            with transaction.atomic():
                order, created = Order.objects.get_or_create(user=user, is_complete=False)
                for pid in product_ids:
                    try:
                        product = Product.objects.get(id=pid, is_active=True)
                        cart_item, created = OrderItem.objects.get_or_create(order=order, product=product)
                        cart_item.quantity = (cart_item.quantity or 0) + 1
                        cart_item.save()
                        added.append(product.name)
                    except Product.DoesNotExist:
                        pass
        except Exception as e:
            return f"Database error: {str(e)}"
        
        if added:
            return f"Successfully added to cart: {', '.join(added)}"
        return "No valid products were found to add."

    history_contents = []
    if chat_history:
        for msg in chat_history:
            history_contents.append(
                types.Content(
                    role=msg['role'],
                    parts=[types.Part.from_text(text=msg['text'])]
                )
            )

    kwargs = {
        'model': 'gemini-flash-lite-latest',
        'config': types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[search_catalog, add_to_cart],
            temperature=0.7,
        )
    }
    
    if history_contents:
        kwargs['history'] = history_contents

    chat = client.chats.create(**kwargs)
    
    response = chat.send_message(user_prompt)
    return response.text if response.text else "Action completed."
