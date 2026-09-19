import sys

# 1. Patch ai_services.py
content_ai = open('myapp/ai_services.py', 'r', encoding='utf-8').read()

new_get_ai = '''
def get_ai_stylist_recommendation(user_prompt: str, user=None, chat_history: list = None) -> dict:
    """
    Processes user request, allows Gemini to query the catalog via tools,
    and returns a structured styling proposal.
    """
    system_instruction = """
    You are an expert personal shopping stylist for an e-commerce platform.
    Your goal is to understand the customer's occasion, taste, and budget, 
    and curate a complete matching bundle using products from our store catalog.
    
    Rules:
    1. ALWAYS call `search_catalog` to inspect what items actually exist in inventory.
    2. NEVER invent fake product IDs or products that aren't returned by `search_catalog`.
    3. Stay strictly within the user's budget if one is stated.
    4. Keep your commentary stylish, concise, and enthusiastic.
    5. If the user tells you they want to buy a product, use the `add_to_cart` tool to add it to their cart.
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

    chat = client.chats.create(
        model='gemini-flash-lite-latest',
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[search_catalog, add_to_cart],
            temperature=0.7,
        )
    )
    
    response = chat.send_message(user_prompt)
    return response.text
'''

start_idx = content_ai.find('def get_ai_stylist_recommendation')
if start_idx != -1:
    content_ai = content_ai[:start_idx] + new_get_ai.strip() + '\n'
    with open('myapp/ai_services.py', 'w', encoding='utf-8') as f:
        f.write(content_ai)
    print("ai_services.py patched.")
else:
    print("Could not find get_ai_stylist_recommendation in ai_services.py")

# 2. Patch views.py
content_views = open('myapp/views.py', 'r', encoding='utf-8').read()
old_call = 'ai_reply = get_ai_stylist_recommendation(user_message)'
new_call = 'ai_reply = get_ai_stylist_recommendation(user_message, request.user)'
if old_call in content_views:
    content_views = content_views.replace(old_call, new_call)
    with open('myapp/views.py', 'w', encoding='utf-8') as f:
        f.write(content_views)
    print("views.py patched.")
else:
    print("Could not find ai_reply call in views.py")
