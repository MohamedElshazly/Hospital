from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from authentication.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
import datetime

# from authentication.models import HospitalManager

class Hospital(models.Model):
    name = models.CharField(_("Hospital Name"), max_length = 225, unique=True)
    address = models.TextField(_("Hospital Address"), null=True)
    phone_num = models.IntegerField()
    manager = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('hospital-details', kwargs={'pk' : self.pk})


class Department(models.Model):
    name = models.CharField(_("Department Name"), max_length = 225, unique=True)
    hospital = models.ForeignKey(Hospital, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    STATUS = (
        ('LIVE', _("LIVE")),
        ('DOWN', _("DOWN"))
    )
    status = models.CharField(_("Equipment Status"), max_length=50, choices=STATUS, default='LIVE')
    name = models.CharField(_("Equipment Name"), max_length = 225, unique=True) #unique=True
    specs = models.TextField(_("Technical Specifications and Standards"))
    quantity = models.IntegerField()
    serial_num = models.IntegerField(unique = True)#add unique = True
    # belongs_to = models.CharField(_("Department"), max_length=255, null=True)
    department = models.ForeignKey(Department, null = True, on_delete=models.SET_NULL)
    hospital = models.ForeignKey(Hospital, null = True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name



###PORT PROXY MODELS INTO NORMAL MODELS, AND USE MULTI INHERITANCE####

class ManagerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.MANAGER)

class EngineerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.ENGINEER)

class DoctorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.DOCTOR)


    

class Manager(User):
    objects = ManagerManager()
   
    def __str__(self):
        return self.username
        
class Engineer(User):
    current_hospital = models.ForeignKey(Hospital, null=True, on_delete=models.CASCADE) #should it be cascade?
    is_busy = models.BooleanField(_("Busy"), default=False)
    total_orders = models.IntegerField(_("Total Work Orders"), default=0)
    orders_done = models.IntegerField(_("Total Work Orders Done"), default=0)
    start_time = models.IntegerField(default=0)
    total_response_time = models.DurationField(_("Total_Response Time"), default=datetime.timedelta())
    average_response_time = models.DurationField(_("Average_Response Time"), default=datetime.timedelta())
    objects = EngineerManager()

   
    def __str__(self):
        return self.username

class Doctor(User):
    current_hospital = models.ForeignKey(Hospital, null=True, on_delete=models.CASCADE) #should it be cascade?
    objects = DoctorManager()
    
    def __str__(self):
        return self.username
