with open('myapp/templates/app.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove drop-shadow from .fab-img
content = content.replace('filter: drop-shadow(0px 8px 12px rgba(0,0,0,0.4));', '/* filter removed for better 3D canvas quality */')

# Enhance model-viewer attributes
old_viewer = '<model-viewer src="{% static \'assets/images/3d-ChatBOT/Chat-Bot-2.O.glb\' %}" alt="3D AI Assistant" auto-rotate rotation-per-second="30deg" interaction-prompt="none" class="fab-img"></model-viewer>'
new_viewer = '<model-viewer src="{% static \'assets/images/3d-ChatBOT/Chat-Bot-2.O.glb\' %}" alt="3D AI Assistant" auto-rotate rotation-per-second="30deg" interaction-prompt="none" class="fab-img" environment-image="neutral" shadow-intensity="1.2" exposure="1.2" camera-orbit="0deg 75deg 105%"></model-viewer>'

if old_viewer in content:
    content = content.replace(old_viewer, new_viewer)
    with open('myapp/templates/app.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated app.html successfully.")
else:
    print("Could not find the target string in app.html.")
