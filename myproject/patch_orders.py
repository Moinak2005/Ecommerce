with open('myapp/templates/orders.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_status = '''{% if order.is_complete %}
                                        <span class="badge bg-success rounded-pill px-3 py-2">Completed</span>
                                    {% else %}
                                        <span class="badge bg-warning text-dark rounded-pill px-3 py-2">Pending</span>
                                    {% endif %}'''

new_status = '''{% if order.status == 'Pending' %}
                                        <span class="badge bg-warning text-dark rounded-pill px-3 py-2">Pending</span>
                                    {% elif order.status == 'Processing' %}
                                        <span class="badge bg-info text-dark rounded-pill px-3 py-2">Processing</span>
                                    {% elif order.status == 'Shipped' %}
                                        <span class="badge bg-primary rounded-pill px-3 py-2">Shipped</span>
                                    {% elif order.status == 'Delivered' %}
                                        <span class="badge bg-success rounded-pill px-3 py-2">Delivered</span>
                                    {% elif order.status == 'Cancelled' %}
                                        <span class="badge bg-danger rounded-pill px-3 py-2">Cancelled</span>
                                    {% else %}
                                        <span class="badge bg-secondary rounded-pill px-3 py-2">{{ order.status }}</span>
                                    {% endif %}
                                    <div class="mt-2" style="font-size: 0.8rem; font-weight: 500;">
                                        <i class="bi bi-geo-alt-fill text-muted"></i> Tracking Updates
                                        <div class="progress mt-1" style="height: 6px;">
                                            {% if order.status == 'Pending' %}
                                                <div class="progress-bar bg-warning" role="progressbar" style="width: 25%"></div>
                                            {% elif order.status == 'Processing' %}
                                                <div class="progress-bar bg-info" role="progressbar" style="width: 50%"></div>
                                            {% elif order.status == 'Shipped' %}
                                                <div class="progress-bar bg-primary progress-bar-striped progress-bar-animated" role="progressbar" style="width: 75%"></div>
                                            {% elif order.status == 'Delivered' %}
                                                <div class="progress-bar bg-success" role="progressbar" style="width: 100%"></div>
                                            {% elif order.status == 'Cancelled' %}
                                                <div class="progress-bar bg-danger" role="progressbar" style="width: 100%"></div>
                                            {% endif %}
                                        </div>
                                    </div>'''

content = content.replace(old_status, new_status)

with open('myapp/templates/orders.html', 'w', encoding='utf-8') as f:
    f.write(content)
