with open('myapp/templates/orders.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We will replace the entire <div class="mb-4 p-3"> containing the stepper-wrapper
pattern = r'<div class="mb-4 p-3">.*?</div>\s*<!-- Items List -->'
new_html = '''<div class="mb-4 p-3">
                                        <style>
                                            .stepper-wrapper {
                                              margin-top: 10px;
                                              display: flex;
                                              justify-content: space-between;
                                              margin-bottom: 20px;
                                              position: relative;
                                            }
                                            .stepper-wrapper::before {
                                                content: "";
                                                position: absolute;
                                                top: 13px;
                                                left: 10%;
                                                width: 80%;
                                                height: 4px;
                                                background-color: #e0e0e0;
                                                z-index: 1;
                                            }
                                            .step-progress-bar {
                                                position: absolute;
                                                top: 13px;
                                                left: 10%;
                                                height: 4px;
                                                background-color: #0d6efd;
                                                z-index: 2;
                                                transition: width 0.4s ease;
                                            }
                                            .stepper-item {
                                              position: relative;
                                              display: flex;
                                              flex-direction: column;
                                              align-items: center;
                                              flex: 1;
                                              z-index: 3;
                                            }
                                            .stepper-item .step-counter {
                                              position: relative;
                                              width: 30px;
                                              height: 30px;
                                              border-radius: 50%;
                                              background-color: #e0e0e0;
                                              display: flex;
                                              justify-content: center;
                                              align-items: center;
                                              margin-bottom: 10px;
                                              color: white;
                                              font-size: 16px;
                                            }
                                            .stepper-item.completed .step-counter {
                                              background-color: #0d6efd;
                                            }
                                            .stepper-item.completed .step-counter::after {
                                                content: "\\2713";
                                            }
                                            .stepper-item .step-name {
                                              font-size: 13px;
                                              font-weight: 600;
                                              color: #6c757d;
                                            }
                                            .stepper-item.completed .step-name {
                                              color: #212529;
                                            }
                                        </style>
                                        
                                        {% if order.status != 'Cancelled' %}
                                        <div class="stepper-wrapper">
                                            {% if order.status == 'Pending' %}
                                                <div class="step-progress-bar" style="width: 0%"></div>
                                            {% elif order.status == 'Processing' %}
                                                <div class="step-progress-bar" style="width: 33%"></div>
                                            {% elif order.status == 'Shipped' %}
                                                <div class="step-progress-bar" style="width: 66%"></div>
                                            {% elif order.status == 'Delivered' %}
                                                <div class="step-progress-bar" style="width: 100%"></div>
                                            {% endif %}
                                        
                                            <div class="stepper-item completed">
                                                <div class="step-counter"></div>
                                                <div class="step-name">Pending</div>
                                            </div>
                                            
                                            <div class="stepper-item {% if order.status == 'Processing' or order.status == 'Shipped' or order.status == 'Delivered' %}completed{% endif %}">
                                                <div class="step-counter"></div>
                                                <div class="step-name">Processing</div>
                                            </div>
                                            
                                            <div class="stepper-item {% if order.status == 'Shipped' or order.status == 'Delivered' %}completed{% endif %}">
                                                <div class="step-counter"></div>
                                                <div class="step-name">Shipped</div>
                                            </div>
                                            
                                            <div class="stepper-item {% if order.status == 'Delivered' %}completed{% endif %}">
                                                <div class="step-counter"></div>
                                                <div class="step-name">Delivered</div>
                                            </div>
                                        </div>
                                        {% else %}
                                        <div class="alert alert-danger text-center fw-bold">
                                            This order has been cancelled.
                                        </div>
                                        {% endif %}
                                    </div>
                                    <!-- Items List -->'''

content = re.sub(pattern, new_html, content, flags=re.DOTALL)

with open('myapp/templates/orders.html', 'w', encoding='utf-8') as f:
    f.write(content)
