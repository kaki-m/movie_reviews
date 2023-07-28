from django import forms
from .models import CustomUser, Review
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email','password1', 'password2']

class LoginForm(AuthenticationForm):
    pass

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content_text','star_num','movie']