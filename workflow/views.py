from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DetailView 
from workflow.models import Ticket
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TicketForm, TicketFormID, AssignEng
from django.urls import reverse_lazy
from med.models import Doctor, Engineer, Equipment, Manager
from authentication.models import User
import time, datetime
# from authentication.models import Engineer

class Submit_Ticket(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'workflow/submit_ticket.html'
    form_class = TicketForm
    context_object_name = 'ticket' 
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(Submit_Ticket, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        form.instance.submitter = self.request.user
        doc = Doctor.objects.get(id = self.request.user.id)
        doc_hos = doc.current_hospital
        eq = doc_hos.equipment_set.filter(name = form.instance.equipment).first()
        eq.status = 'DOWN'
        eq.save()
        # form.save()
        # form.instance.status = 'DOWN'
        return super().form_valid(form) 


class Submit_Ticket_Using_Id(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = 'workflow/submit_ticket_id.html'

    form_class = TicketFormID
    context_object_name = 'ticket' 
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.submitter = self.request.user
        eq = Equipment.objects.get(id = self.kwargs['pk'])
        eq.status = 'DOWN'
        eq.save()
        form.instance.equipment = Equipment.objects.get(id = self.kwargs['pk'])
        return super().form_valid(form) 


class List_Tickets(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'workflow/list_tickets.html'

    def queryset(self):
        if(self.request.user.type == 'ENGINEER'):
            eng = Engineer.objects.get(id = self.request.user.id)
            eng_hos = eng.current_hospital 
            dep_list = eng_hos.department_set.all()
            object_list = [ticket for q1 in dep_list for eq in q1.equipment_set.all() for ticket in eq.ticket_set.all()]
            return object_list
        elif(self.request.user.type == 'DOCTOR'):
            doc = Doctor.objects.get(id = self.request.user.id)
            doc_hos = doc.current_hospital 
            dep_list = doc_hos.department_set.all()
            object_list = [ticket for q1 in dep_list for eq in q1.equipment_set.all() for ticket in eq.ticket_set.all()]
            return object_list
        else:
            man = Manager.objects.get(id = self.request.user.id)
            dep_list = man.hospital.department_set.all()
            object_list = [ticket for q1 in dep_list for eq in q1.equipment_set.all() for ticket in eq.ticket_set.all()]
            return object_list
    
    # def get_context_data(self, **kwargs):
    #     context = super(List_Tickets, self).get_context_data(**kwargs)
    #     man = Manager.objects.get(id = self.request.user.id)
    #     context['engineers'] = man.hospital.engineer_set.filter(is_busy=False)
    #     return context

class Ticket_Details(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'workflow/ticket_details.html'

    def get_context_data(self, **kwargs):
        context = super(Ticket_Details, self).get_context_data(**kwargs)
        context['ticket'] = Ticket.objects.get(id = self.kwargs['pk'])
        try:
            context['engineer'] = Engineer.objects.get(id = self.request.user.id)
        except:
            pass
        return context

class Assign_Engineer(LoginRequiredMixin, UpdateView):
    model = Ticket
    template_name = 'workflow/assign.html'
    form_class = AssignEng
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super(Assign_Engineer, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        eng = form.instance.user
        #subtract totalworkorder by 1 from user already have it
        eng.is_busy = True; 
        eng.total_orders += 1
        eng.save()
        return super().form_valid(form)


class Engineer_Work(LoginRequiredMixin, ListView):
    model = Ticket 
    template_name = 'workflow/eng_work.html'

    def get_queryset(self):
        eng = Engineer.objects.get(id = self.request.user.id)
        object_list = eng.ticket_set.all()
        return object_list
    
    def get_context_data(self, **kwargs):
        context = super(Engineer_Work, self).get_context_data(**kwargs)
        context['engineer'] = Engineer.objects.get(id = self.request.user.id)
        return context

class List_Employees(LoginRequiredMixin, ListView):
    model = User
    template_name ='workflow/list_employees.html'

    def get_queryset(self):
        current_man = Manager.objects.get(id = self.request.user.id)
        engs = current_man.hospital.engineer_set.all()
        docs = current_man.hospital.doctor_set.all()
        object_list = [eng for eng in engs]
        object_list += [doc for doc in docs]
        return object_list


def Work_Process(request, pk, pk2):
    eng = Engineer.objects.get(id = request.user.id)
    current_time_seconds = round(time.time())
    if pk == 1: 
        eng.start_time = current_time_seconds
        eng.save()
        return redirect('eng-work') 
    
    current_time_seconds_end = current_time_seconds - eng.start_time
    response_time_delta = datetime.timedelta(seconds=current_time_seconds_end)
    eng.start_time = 0
    eng.orders_done += 1
    eng.total_response_time += response_time_delta
    eng.average_response_time = (eng.total_response_time / eng.orders_done)
    current_ticket = Ticket.objects.get(id = pk2)
    current_ticket.response_time = response_time_delta
    current_ticket.status = 'CLOSED'
    current_ticket.equipment.status = 'LIVE'
    current_ticket.save()
    current_ticket.equipment.save()
    eng.save()
    return redirect('eng-work') 



