from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login

import pdb

class UserManager(models.Manager):

    def create_user(self, request, user_profile, signup_form):
        u = User.objects.create_user(signup_form.cleaned_data['email'], signup_form.cleaned_data['email'], signup_form.cleaned_data['password'])
        u.first_name = signup_form.cleaned_data['first_name']
        u.last_name = signup_form.cleaned_data['last_name']
        u.save()
        user_profile.user = u
        user_profile.save()
        login(request, user)

    def login_user(self, request, login_form):
        user = authenticate(username=login_form.cleaned_data['email'], password=login_form.cleaned_data['password'])
        if user is not None:
            login(request, user)
        return user.is_authenticated()

    def logout_user(self, request):
        logout(request)