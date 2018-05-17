from django import forms
from .models import UserProfile

class UserProfileForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(label='First Name', max_length=150,
                 empty_value=None, required=False)
    last_name = forms.CharField(label='Last Name', max_length=150,
                  empty_value=None, required=False)
