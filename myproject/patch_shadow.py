with open('myapp/templates/app.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update the button class to remove shadow-lg and rounded-circle
content = content.replace('class="rounded-circle shadow-lg fab-button"', 'class="fab-button"')

# Update the img tag to remove border, box-shadow, and border-radius, and use the new transparent image
old_img = '''<img src="{% static 'assets/images/3d-ChatBOT/11529294.jpg' %}" alt="AI Assistant" class="fab-img">'''
new_img = '''<img src="{% static 'assets/images/3d-ChatBOT/robot_transparent.png' %}" alt="AI Assistant" class="fab-img">'''
content = content.replace(old_img, new_img)

# Update the CSS for fab-img to use drop-shadow instead of box-shadow
old_css = '''
.fab-img {
    width: 80px; 
    height: 80px; 
    border-radius: 50%; 
    object-fit: cover; 
    border: none; 
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}
'''

new_css = '''
.fab-img {
    width: 90px; 
    height: 90px; 
    object-fit: contain; 
    filter: drop-shadow(0px 8px 12px rgba(0,0,0,0.4));
}
'''
if old_css.strip() in content:
    content = content.replace(old_css.strip(), new_css.strip())
else:
    # Try another format if spaces differ
    import re
    content = re.sub(r'\.fab-img\s*\{[^}]+\}', new_css.strip(), content)

with open('myapp/templates/app.html', 'w', encoding='utf-8') as f:
    f.write(content)
