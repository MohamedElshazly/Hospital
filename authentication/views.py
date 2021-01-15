from django.shortcuts import render, redirect
from .forms import ManagerSignUpForm, EngineerSignUpForm, DoctorSignUpForm
from django.views.generic import TemplateView, ListView
from med.models import Hospital

class SignUpView(TemplateView):
    template_name = 'authentication/register.html'

def ManagerRegister(request):
    if request.method == 'POST':
        form = ManagerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = ManagerSignUpForm()
    return render(request, 'authentication/register_form.html', {'form' : form})

def EngineerRegister(request):
    if request.method == 'POST':
        form = EngineerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = EngineerSignUpForm()
    return render(request, 'authentication/register_form.html', {'form' : form})

def DoctorRegister(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = DoctorSignUpForm()
    return render(request, 'authentication/register_form.html', {'form' : form})

