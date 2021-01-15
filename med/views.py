from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView, ListView, DetailView, UpdateView
from .models import Engineer, Hospital, Doctor, Equipment, Manager
from .forms import HospitalForm
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


def JoinHospitalView(request, pk):
    if(request.user.type == 'ENGINEER'):
        eng = Engineer.objects.get(id = request.user.id)
        eng.current_hospital = Hospital.objects.get(id=pk)
        eng.in_hospital = True
        eng.save()
        return redirect('home')
    if(request.user.type == 'DOCTOR'):
        doc = Doctor.objects.get(id = request.user.id)
        doc.current_hospital = Hospital.objects.get(id=pk)
        doc.in_hospital = True
        doc.save()
        return redirect('home')
    

class CreateHospitalView(LoginRequiredMixin, CreateView):
    model = Hospital
    template_name = 'med/register_hospital.html'
    form_class = HospitalForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super().form_valid(form)

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