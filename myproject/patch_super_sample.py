with open('myapp/templates/app.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We will replace everything from .fab-container { to /* filter removed for better 3D canvas quality */ }

old_css = re.search(r'(\.fab-container \{.*?\/\* filter removed for better 3D canvas quality \*\/[ \t]*\n?\})', content, re.DOTALL)

if old_css:
    new_css = '''.fab-container {
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
        width: 100px;
        height: 100px;
        position: relative;
    }
    .fab-img {
        width: 400px;
        height: 400px;
        position: absolute;
        bottom: -20px;
        right: -20px;
        transform: scale(0.35); /* Super-sample down for retina sharpness */
        transform-origin: bottom right;
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        pointer-events: none;
    }
    .fab-button:hover .fab-img {
        transform: scale(0.40); /* Hover effect scaled up slightly */
    }'''
    
    content = content.replace(old_css.group(1), new_css)
    with open('myapp/templates/app.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated CSS successfully.")
else:
    print("Could not find the target CSS block.")
