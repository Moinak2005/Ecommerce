with open('myapp/templates/app.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('under $15', 'under ₹500')

with open('myapp/templates/app.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('myapp/templates/shop.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('placeholder="Min $"', 'placeholder="Min ₹"')
content = content.replace('placeholder="Max $"', 'placeholder="Max ₹"')

with open('myapp/templates/shop.html', 'w', encoding='utf-8') as f:
    f.write(content)
