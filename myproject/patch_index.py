with open('myapp/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
old_section = re.search(r'(<div class="bg-secondary text-light py-5 my-5"[^\n]*>.*?Just Sign Up & Register it now to become member.</p>.*?<form>.*?<input.*?name="name".*?<input.*?name="email".*?</form>.*?</div>\s*</div>\s*</div>)', content, re.DOTALL)

if old_section:
    new_html = '{% if not user.is_authenticated %}\n' + old_section.group(1).replace('<form>', '<form method="GET" action="{% url \'register\' %}">') + '\n{% endif %}'
    content = content.replace(old_section.group(1), new_html)
    with open('myapp/templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Updated index.html')
else:
    print('Could not find the section')
