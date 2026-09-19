(function() {
    'use strict';

    function init() {
        // Find the image file input — Django names it "id_image"
        var fileInput = document.getElementById('id_image');
        if (!fileInput) return;

        // --- Move the "Currently: filename □ Clear" line below the file input ---
        var wrapper = fileInput.closest('.file-upload') || fileInput.parentNode;
        // Django's ClearableFileInput puts "Currently:" as a text node + <a> + checkbox
        // all before the <br> that precedes "Change:". Collect those nodes.
        var currentlyNodes = [];
        var node = wrapper.firstChild;
        var brFound = false;
        while (node) {
            var next = node.nextSibling;
            // Stop collecting once we hit the first <br> (separator before "Change:")
            if (node.nodeName === 'BR') {
                brFound = true;
                // Also grab the "Change:" label line's <br> to remove it
                wrapper.removeChild(node);
                break;
            }
            currentlyNodes.push(node);
            node = next;
        }

        // Find the help text element (rendered as <div class="help"> after the wrapper)
        var fieldRow = wrapper.closest('.form-row') || wrapper.parentNode;
        var helpText = fieldRow.querySelector('.help');

        if (brFound && currentlyNodes.length > 0) {
            // Create a container for the relocated "Currently:" line
            var currentlyDiv = document.createElement('div');
            // Reset styles so it doesn't inherit help text styling
            currentlyDiv.style.cssText = 'margin-top:8px; color:var(--body-fg, #333); font-size:13px; font-style:normal; font-weight:normal; line-height:1.5;';
            currentlyNodes.forEach(function(n) {
                currentlyDiv.appendChild(n);
            });
            // Append inside helpText to guarantee exact horizontal alignment
            if (helpText) {
                helpText.appendChild(currentlyDiv);
            } else {
                wrapper.parentNode.insertBefore(currentlyDiv, wrapper.nextSibling);
            }
        }

        // --- Build the selected-file preview container ---
        var container = document.createElement('div');
        container.id = 'selected-image-preview';
        // Reset styles so it doesn't inherit help text styling
        container.style.cssText = 'margin-top:10px; display:none; color:var(--body-fg, #333); font-size:13px; font-style:normal; font-weight:normal; line-height:1.5;';

        container.innerHTML =
            '<div style="display:flex;align-items:center;gap:10px;">' +
                '<img id="selected-preview-img" src="" style="max-height:150px;max-width:250px;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.15);object-fit:contain;" />' +
                '<a id="selected-preview-eye" href="#" target="_blank" title="View selected image full size" style="' +
                    'display:inline-flex;align-items:center;justify-content:center;' +
                    'width:34px;height:34px;border-radius:50%;background:#417690;color:#fff;' +
                    'text-decoration:none;font-size:18px;flex-shrink:0;"' +
                '>&#128065;</a>' +
            '</div>' +
            '<p style="margin:6px 0 0;font-size:12px;color:#999;font-style:italic;">Selected file preview (not yet saved)</p>';

        // Append inside helpText to guarantee exact horizontal alignment
        if (helpText) {
            helpText.appendChild(container);
        } else {
            var anchor = (typeof currentlyDiv !== 'undefined' && currentlyDiv) ? currentlyDiv : wrapper;
            anchor.parentNode.insertBefore(container, anchor.nextSibling);
        }

        // Listen for file selection
        fileInput.addEventListener('change', function() {
            var preview = document.getElementById('selected-image-preview');
            var img = document.getElementById('selected-preview-img');
            var eyeBtn = document.getElementById('selected-preview-eye');

            if (fileInput.files && fileInput.files[0]) {
                var file = fileInput.files[0];

                // Only preview image files
                if (!file.type.startsWith('image/')) {
                    preview.style.display = 'none';
                    return;
                }

                var reader = new FileReader();
                reader.onload = function(e) {
                    img.src = e.target.result;
                    // Eye button opens the full-size image in a new tab
                    eyeBtn.href = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            } else {
                preview.style.display = 'none';
            }
        });
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
