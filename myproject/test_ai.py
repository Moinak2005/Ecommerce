import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import User
from myapp.ai_services import get_ai_stylist_recommendation

# Get a test user
user = User.objects.first()
print(f'Testing with user: {user}')

chat_history = [
    {'role': 'user', 'text': 'ingredients of paneer lababdar'},
    {'role': 'model', 'text': 'I found Paneer (ID: 12). Do you want me to add it to your cart?'}
]

reply = get_ai_stylist_recommendation('yes', user, chat_history)
print(f'AI Reply: {reply}')
