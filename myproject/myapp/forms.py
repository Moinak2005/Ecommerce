from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

from .models import UserProfile

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20, required=True, label="Phone Number")
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True, label="Address")
    city = forms.CharField(max_length=100, required=True, label="City")
    zip_code = forms.CharField(max_length=20, required=True, label="Zip Code")

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'city', 'zip_code']
