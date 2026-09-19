with open('myapp/templates/orders.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('<div class="step-name">Processing</div>', '<div class="step-name">Shipped </div>')
content = content.replace('<div class="step-name">Shipped</div>', '<div class="step-name">Out for delivery</div>')

with open('myapp/templates/orders.html', 'w', encoding='utf-8') as f:
    f.write(content)
