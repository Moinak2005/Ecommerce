with open('myapp/templates/register.html', 'r', encoding='utf-8') as f:
    content = f.read()

script_to_add = '''
<script>
document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const fullName = urlParams.get('name');
    const email = urlParams.get('email');
    
    if (email) {
        const emailField = document.getElementById('id_email');
        if (emailField) {
            emailField.value = email;
            // Optionally trigger input event for validation
            emailField.dispatchEvent(new Event('input'));
        }
    }
    
    if (fullName) {
        const nameParts = fullName.trim().split(/\s+/);
        const firstName = nameParts[0] || '';
        const lastName = nameParts.slice(1).join(' ') || ''; // Everything else is last name
        
        const firstNameField = document.getElementById('id_first_name');
        const lastNameField = document.getElementById('id_last_name');
        
        if (firstNameField && firstName) {
            firstNameField.value = firstName;
            firstNameField.dispatchEvent(new Event('input'));
        }
        if (lastNameField && lastName) {
            lastNameField.value = lastName;
            lastNameField.dispatchEvent(new Event('input'));
        }
    }
});
</script>
'''

if 'const urlParams = new URLSearchParams' not in content:
    content = content.replace('{% endblock content %}', script_to_add + '\n{% endblock content %}')
    with open('myapp/templates/register.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated register.html")
else:
    print("Already updated.")
