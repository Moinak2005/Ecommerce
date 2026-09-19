import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import User, Order, OrderItem
user = User.objects.first()
order = Order.objects.filter(user=user, is_complete=False).first()
if order:
    for item in order.orderitem_set.all():
        print(f'Cart Item: {item.product.name} (ID: {item.product.id}) - Qty: {item.quantity}')
else:
    print('No active order')
