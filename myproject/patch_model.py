with open('myapp/templates/app.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_img = '''<img src="{% static 'assets/images/3d-ChatBOT/robot_transparent.png' %}" alt="AI Assistant" class="fab-img">'''
new_model = '''<model-viewer src="{% static 'assets/images/3d-ChatBOT/3d_demo_6.glb' %}" alt="3D AI Assistant" auto-rotate rotation-per-second="30deg" interaction-prompt="none" class="fab-img"></model-viewer>'''

content = content.replace(old_img, new_model)

if 'model-viewer.min.js' not in content:
    script_tag = '''<script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/4.0.0/model-viewer.min.js"></script>\n</body>'''
    content = content.replace('</body>', script_tag)

with open('myapp/templates/app.html', 'w', encoding='utf-8') as f:
    f.write(content)
