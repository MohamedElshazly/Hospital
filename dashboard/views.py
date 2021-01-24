from django.shortcuts import render, redirect
from med.models import Manager, Engineer, Doctor
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm


# Create your views here.
def home(request):
    try:
        if(request.user.type == 'ENGINEER'):
            eng = Engineer.objects.get(id = request.user.id)
            return render(request, template_name='dashboard/home.html', context={'user' : eng})
        elif(request.user.type == 'DOCTOR'):
            doc = Doctor.objects.get(id = request.user.id)
            return render(request, template_name='dashboard/home.html', context={'user' : doc})
    except:
        return render(request, template_name='dashboard/home.html')
    man = Manager.objects.get(id = request.user.id)
    return render(request, template_name='dashboard/home.html', context={'user' : man})
    
@login_required
def profile(request):
    if(request.user.type == 'ENGINEER'):
        eng = Engineer.objects.get(id = request.user.id)
        return render(request, template_name='dashboard/profile.html', context={'user' : eng})
    elif(request.user.type == 'DOCTOR'):
        doc = Doctor.objects.get(id = request.user.id)
        return render(request, template_name='dashboard/profile.html', context={'user' : doc})
    else:
        return render(request, template_name='dashboard/profile.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            # messages.success(request, f'Account Info Updated!!')
            return redirect('profile')
        else:
            # messages.faliure(request, f'An error has occured!')
            return redirect('profile')
              
    u_form = UserUpdateForm(instance=request.user)

    context = {
            'u_form' : u_form
            }
    return render(request, "dashboard/update_profile.html", context)  