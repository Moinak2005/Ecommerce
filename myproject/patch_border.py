with open('myapp/templates/app.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("border: 4px solid #7eb62c;", "border: none;")

with open('myapp/templates/app.html', 'w', encoding='utf-8') as f:
    f.write(content)
