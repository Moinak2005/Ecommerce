import sys

# 1. Update ai_services.py
with open('myapp/ai_services.py', 'r', encoding='utf-8') as f:
    ai_content = f.read()

old_sys_inst = '''system_instruction = """
    You are an expert personal shopping stylist for an e-commerce platform.
    Your goal is to understand the customer's occasion, taste, and budget, 
    and curate a complete matching bundle using products from our store catalog.
    
    Rules:
    1. ALWAYS call `search_catalog` to inspect what items actually exist in inventory.
    2. NEVER invent fake product IDs or products that aren't returned by `search_catalog`.
    3. Stay strictly within the user's budget if one is stated.
    4. Keep your commentary stylish, concise, and enthusiastic.
    5. If the user tells you they want to buy a product, use the `add_to_cart` tool to add it to their cart.
    """'''

new_sys_inst = '''system_instruction = """
    You are a friendly and expert assistant for an Organic Grocery Store.
    Your goal is to help customers find fresh organic produce, groceries, and ingredients for their recipes, while staying within their budget.
    
    Rules:
    1. ALWAYS call `search_catalog` to inspect what items actually exist in our organic inventory.
    2. NEVER invent fake product IDs or products that aren't returned by `search_catalog`.
    3. Stay strictly within the user's budget if one is stated.
    4. Keep your commentary helpful, concise, and enthusiastic about healthy eating.
    5. If the user tells you they want to buy a product, use the `add_to_cart` tool to add it to their cart.
    """'''

ai_content = ai_content.replace(old_sys_inst, new_sys_inst)
with open('myapp/ai_services.py', 'w', encoding='utf-8') as f:
    f.write(ai_content)

# 2. Update app.html
with open('myapp/templates/app.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

html_content = html_content.replace('✨ AI Stylist', '🛒 AI Assistant')
html_content = html_content.replace('✨ Personal AI Stylist', '🛒 Organic Store Assistant')
html_content = html_content.replace("Tell me what occasion or vibe you're dressing for (e.g., <em>\"Sunday brunch in Goa under ₹3,500\"</em>).", "Tell me what you're cooking or looking for (e.g., <em>\"Ingredients for a healthy salad under $15\"</em>).")
html_content = html_content.replace('Ask your stylist...', 'Ask your assistant...')
html_content = html_content.replace('<strong>Stylist:</strong>', '<strong>Assistant:</strong>')

with open('myapp/templates/app.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Update complete!")
