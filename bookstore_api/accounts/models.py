from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
admin.site.register(CustomUser)