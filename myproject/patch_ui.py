with open('myapp/templates/app.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_script = """    if (data.reply) {
        chatBox.innerHTML += `<div class="mb-3 text-start"><strong>Assistant:</strong><div class="mt-1">${data.reply.replace(/\\n/g, '<br>')}</div></div>`;
    } else if (data.error) {"""

new_script = """    if (data.reply) {
        chatBox.innerHTML += `<div class="mb-3 text-start"><strong>Assistant:</strong><div class="mt-1">${data.reply.replace(/\\n/g, '<br>')}</div></div>`;
        
        // Update the cart UI in the background
        fetch(window.location.href)
        .then(res => res.text())
        .then(html => {
            let parser = new DOMParser();
            let doc = parser.parseFromString(html, 'text/html');
            
            let newBadge = doc.getElementById('cart-badge');
            let oldBadge = document.getElementById('cart-badge');
            if (newBadge && oldBadge) {
                oldBadge.innerHTML = newBadge.innerHTML;
                oldBadge.className = newBadge.className;
            }
            
            let newOffcanvas = doc.querySelector('#offcanvasCart .offcanvas-body');
            let oldOffcanvas = document.querySelector('#offcanvasCart .offcanvas-body');
            if (newOffcanvas && oldOffcanvas) {
                oldOffcanvas.innerHTML = newOffcanvas.innerHTML;
            }
            
            // Also update the cart items count in desktop header if it exists
            let newBadgeDesktop = doc.querySelector('.badge.bg-primary.rounded-pill');
            let oldBadgeDesktop = document.querySelector('.badge.bg-primary.rounded-pill');
            if (newBadgeDesktop && oldBadgeDesktop && oldBadgeDesktop.id !== 'cart-badge') {
                oldBadgeDesktop.innerHTML = newBadgeDesktop.innerHTML;
            }
        });
        
    } else if (data.error) {"""

if old_script in content:
    content = content.replace(old_script, new_script)
    with open('myapp/templates/app.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated app.html successfully.")
else:
    print("Could not find the target string in app.html.")
