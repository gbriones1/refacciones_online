from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from app.account.managers import UserManager

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    street1 = models.CharField(max_length=300, blank=True, null=True)
    street2 = models.CharField(max_length=300, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    objects = models.Manager()

    user_manager = UserManager()

    def create_user(self, request, form):
    	return UserProfile.user_manager.create_user(self, request, self, form)

    def login_user(self, request, form):
        return UserProfile.user_manager.login_user(request, form)

    def logout_user(self, request):
        return UserProfile.user_manager.logout_user(request)

    