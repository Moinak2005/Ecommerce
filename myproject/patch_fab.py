with open('myapp/templates/app.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_btn = '''<div id="ai-stylist-fab" style="position: fixed; bottom: 25px; right: 25px; z-index: 9999;">
    <button onclick="toggleStylist()" class="btn btn-dark rounded-circle shadow-lg p-3" style="border: none; background: #333;">
        🛒 AI Assistant
    </button>
</div>'''

new_btn = '''<div id="ai-stylist-fab" style="position: fixed; bottom: 25px; right: 25px; z-index: 9999;">
    <button onclick="toggleStylist()" class="rounded-circle shadow-lg" style="border: none; background: transparent; padding: 0; transition: transform 0.2s; cursor: pointer;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
        <img src="{% static 'assets/images/chatbot-icon.jpg' %}" alt="AI Assistant" style="width: 75px; height: 75px; border-radius: 50%; object-fit: cover; border: 3px solid #7eb62c; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
    </button>
</div>'''

content = content.replace(old_btn, new_btn)

with open('myapp/templates/app.html', 'w', encoding='utf-8') as f:
    f.write(content)
