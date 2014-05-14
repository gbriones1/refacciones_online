from django import forms            
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm      



class SignUpForm(forms.Form):
    email = forms.EmailField(required = True)
    password = forms.CharField(required = True)
    first_name = forms.CharField(required = False)
    last_name = forms.CharField(required = False)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')  


class LogInForm(forms.Form):
    email = forms.EmailField(required = True)
    password = forms.CharField(required = True)

    class Meta:
        model = User
        fields = ('email', 'password')        
