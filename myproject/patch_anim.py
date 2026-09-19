with open('myapp/templates/app.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_btn = '''<div id="ai-stylist-fab" style="position: fixed; bottom: 25px; right: 25px; z-index: 9999;">
    <button onclick="toggleStylist()" class="rounded-circle shadow-lg" style="border: none; background: transparent; padding: 0; transition: transform 0.2s; cursor: pointer;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
        <img src="{% static 'assets/images/chatbot-icon.jpg' %}" alt="AI Assistant" style="width: 75px; height: 75px; border-radius: 50%; object-fit: cover; border: 3px solid #7eb62c; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
    </button>
</div>'''

new_btn = '''
<style>
@keyframes robotFloat {
    0% { transform: translateY(0px) rotate(0deg); }
    33% { transform: translateY(-8px) rotate(4deg); }
    66% { transform: translateY(-4px) rotate(-3deg); }
    100% { transform: translateY(0px) rotate(0deg); }
}
.fab-container {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 9999;
    animation: robotFloat 4s ease-in-out infinite;
}
.fab-button {
    border: none;
    background: transparent;
    padding: 0;
    cursor: pointer;
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.fab-button:hover {
    transform: scale(1.15);
}
.fab-img {
    width: 80px; 
    height: 80px; 
    border-radius: 50%; 
    object-fit: cover; 
    border: 4px solid #7eb62c; 
    box-shadow: 0 8px 20px rgba(0,0,0,0.3);
}
</style>
<div id="ai-stylist-fab" class="fab-container">
    <button onclick="toggleStylist()" class="rounded-circle shadow-lg fab-button">
        <img src="{% static 'assets/images/chatbot-icon.jpg' %}" alt="AI Assistant" class="fab-img">
    </button>
</div>
'''

if old_btn in content:
    content = content.replace(old_btn, new_btn.strip())
    with open('myapp/templates/app.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched successfully.")
else:
    print("Could not find the old button to replace.")
