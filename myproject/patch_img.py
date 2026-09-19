with open('myapp/templates/app.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("{% static 'assets/images/chatbot-icon.jpg' %}", "{% static 'assets/images/3d-ChatBOT/11529294.jpg' %}")

with open('myapp/templates/app.html', 'w', encoding='utf-8') as f:
    f.write(content)
