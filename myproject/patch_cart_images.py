for filename in ['myapp/templates/cart.html', 'myapp/templates/app.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content.replace(
        '{% static item.product.image_url %}', 
        '{% if item.product.image %}{{ item.product.image.url }}{% else %}{% static item.product.image_url %}{% endif %}'
    )
    
    if content != new_content:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {filename}')
    else:
        print(f'No changes needed for {filename}')
