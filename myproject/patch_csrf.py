content = open('myapp/templates/app.html', encoding='utf-8').read()
content = content.replace("'X-CSRFToken': '{{ csrf_token }}'", "'X-CSRFToken': getCookie('csrftoken')")

js_fix = '''
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
'''
if 'function getCookie' not in content:
    content = content.replace('async function sendStylistMessage()', js_fix + '\\nasync function sendStylistMessage()')

with open('myapp/templates/app.html', 'w', encoding='utf-8') as f:
    f.write(content)
