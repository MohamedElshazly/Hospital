from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, ListView, DetailView, UpdateView
from .models import Engineer, Hospital, Doctor, Equipment, Manager, Notifications, Department, Company
from .forms import HospitalForm, CreateCompanyForm
from django.urls import reverse_lazy
from django.db.models import Q
from med.forms import JoinHospitalForm
from authentication.models import User
from workflow.models import Ticket
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
import datetime
from xhtml2pdf import pisa 

class SearchHospitalView(LoginRequiredMixin, ListView):
    model = Hospital
    template_name = 'med/hospital_search.html'

    def get_queryset(self):
        object_list = Hospital.objects.all()
        return object_list

class EquipmentListView(LoginRequiredMixin, ListView):
    model = Equipment
    template_name = 'med/equipment_list.html'

    def get_queryset(self):
        if(self.request.user.type == 'ENGINEER'):
            eng = Engineer.objects.get(id = self.request.user.id)
            eng_hos = eng.current_hospital 
            object_list = eng_hos.equipment_set.all()
            # object_list = [eq for q1 in dep_list for eq in q1.equipment_set.all()]
            return object_list
        elif(self.request.user.type == 'DOCTOR'):
            doc = Doctor.objects.get(id = self.request.user.id)
            doc_hos = doc.current_hospital 
            object_list = doc_hos.equipment_set.all()
            # object_list = [eq for q1 in dep_list for eq in q1.equipment_set.all()]
            return object_list
        else:
            man = Manager.objects.get(id = self.request.user.id)
            object_list = man.hospital.equipment_set.all()
            # object_list = [eq for q1 in dep_list for eq in q1.equipment_set.all()]
            return object_list

class DepartmentListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'med/department_list.html'

    def get_queryset(self):
        if(self.request.user.type == 'ENGINEER'):
            eng = Engineer.objects.get(id = self.request.user.id)
            eng_hos = eng.current_hospital 
            object_list = eng_hos.department_set.all()
            return object_list
        elif(self.request.user.type == 'DOCTOR'):
            doc = Doctor.objects.get(id = self.request.user.id)
            doc_hos = doc.current_hospital 
            object_list = doc_hos.department_set.all()
            return object_list
        else:
            man = Manager.objects.get(id = self.request.user.id)
            object_list = man.hospital.department_set.all()
            return object_list

class  SearchHospitalResultsView(LoginRequiredMixin, ListView):
    model = Hospital
    template_name = 'med/hospital_search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Hospital.objects.filter(
            Q(name__icontains=query) | Q(address__icontains=query)
        )
        return object_list


class HospitalDetailsView(LoginRequiredMixin, DetailView):
    model = Hospital 
    template_name = 'med/hospital_details.html'
    context_object_name = 'hospital'
    #can I send a specific context here ??

class EquipmentDetailsView(LoginRequiredMixin, DetailView):
    model = Equipment 
    template_name = 'med/equipment_details.html'
    context_object_name = 'equipment'
    #can I send a specific context here ??

    def get_context_data(self, **kwargs):
        context = super(EquipmentDetailsView, self).get_context_data(**kwargs)
        context['equipment'] = Equipment.objects.get(id = self.kwargs['pk'])
        try:
            context['ticket'] = Ticket.objects.get(Q(equipment = Equipment.objects.get(id = self.kwargs['pk'])), Q(status = 'OPEN'))
            context['engineer'] = Engineer.objects.get(id = self.request.user.id)
        except:
            pass
        return context


def JoinHospitalView(request, uid):
    man = Manager.objects.get(id = request.user.id)
    user = User.objects.get(id = uid)
    try:
        eng = Engineer.objects.get(id = uid)
        eng.is_approved = True 
        eng.current_hospital = man.hospital
        user.in_hospital = True
        Notifications.objects.get(user = user).delete() 
        eng.save()
        user.save()
        return redirect('home')
    except:
        doc = Doctor.objects.get(id = uid)
        doc.is_approved = True 
        doc.current_hospital = man.hospital        
        user.in_hospital = True 
        Notifications.objects.get(user = user).delete() 
        doc.save()
        user.save()
        return redirect('home')

def RequestJoinHospitalView(request, hid, uid):
    user = User.objects.get(id = uid)
    hospital = Hospital.objects.get(id = hid)
    try :
        #check if use already submitted a request, and delete it if he did
        Notifications.objects.get(user=user).delete()
        #create new notification
        Notifications.objects.create(user=user, hospital=hospital)
        return redirect('home')
    except:
        #if he didn't already have a request, just create a new one
        Notifications.objects.create(user=user, hospital=hospital)
        return redirect('home')
        

class NotificationsListView(LoginRequiredMixin, ListView):
    model = Notifications
    template_name = 'med/list_notifications.html'

    def get_queryset(self):
        man_hos = Manager.objects.get(id = self.request.user.id).hospital
        object_list = Notifications.objects.filter(hospital=man_hos)
        return object_list



    #Add a test 
    
class CreateHospitalView(LoginRequiredMixin, CreateView):
    model = Hospital
    template_name = 'med/register_hospital.html'
    form_class = HospitalForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super().form_valid(form)

class List_Create_CompanyView(LoginRequiredMixin, CreateView):
    model = Company
    template_name = 'med/list_create_company.html'
    form_class = CreateCompanyForm
    success_url = reverse_lazy('list-create-company')

    def form_valid(self, form):
        eng_hos = Engineer.objects.get(id = self.request.user.id).current_hospital
        form.instance.hospital = eng_hos
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        eng_hos = Engineer.objects.get(id = self.request.user.id).current_hospital
        context["companies"] = Company.objects.filter(hospital = eng_hos)
        return context

def generate_PDF(request, pk):
    data = {}
    data['ticket'] = Ticket.objects.get(id = pk)
    template = get_template('workflow/ticket_details.html')
    html  = template.render(data)

    file = open('test.pdf', "w+b")
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
            encoding='utf-8')

    file.seek(0)
    pdf = file.read()
    file.close()            
    return HttpResponse(pdf, 'application/pdf')