from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from django import forms


class User(AbstractUser):
    
    class Types(models.TextChoices):
        MANAGER = "MANAGER", "manager"
        ENGINEER = "ENGINEER", "engineer"
        DOCTOR = "DOCTOR", "doctor"
    


    type = models.CharField(_("Type"), max_length= 50, choices=Types.choices, default = Types.MANAGER)
    in_hospital = models.BooleanField(_("Currently registered in a hospital"), default=False)
    
    