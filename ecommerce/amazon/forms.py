from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email'] # password1 and password2 are handled by UserCreationForm automatically

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        # This tells Django NOT to show these fields in the HTML
        # Because we set them manually in views.py
        exclude = ['user', 'total_amount']
