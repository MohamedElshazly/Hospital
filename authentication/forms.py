from django import forms
from django.contrib.auth.forms import UserCreationForm
from med.models import Manager, Doctor, Engineer

class ManagerSignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Manager
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def save(self):
        user = super().save(commit=False)
        user.type = 'MANAGER'
        user.save()
        return user

class EngineerSignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Engineer
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def save(self):
        user = super().save(commit=False)
        user.type = 'ENGINEER'
        user.save()
        return user

class DoctorSignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Doctor
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def save(self):
        user = super().save(commit=False)
        user.type = 'DOCTOR'
        user.save()
        return user
