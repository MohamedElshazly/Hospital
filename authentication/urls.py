from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ManagerRegister, EngineerRegister, DoctorRegister
from .views import SignUpView
from med.views import JoinHospitalView, RequestJoinHospitalView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name = 'authentication/login.html'), name ='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authentication/logout.html'), name ='logout'),
    path('register/', SignUpView.as_view(), name ='register'),
    path('manager-register/', ManagerRegister, name ='manager-register'),
    path('engineer-register/', EngineerRegister, name ='engineer-register'),
    path('doctor-register/', DoctorRegister, name ='doctor-register'),
    path('request-join-hospital/<int:hid>/<int:uid>/', RequestJoinHospitalView, name ='request-join-hospital'),
    path('join-hospital/<int:uid>/', JoinHospitalView, name ='join-hospital')

   

]
