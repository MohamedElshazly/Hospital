from django import forms
from .models import Ticket
from med.models import Equipment
from med.models import Department, Doctor, Engineer, Manager

class CustomMCF(forms.ModelChoiceField):
    def label_from_instance(self, equipment):
        return f'{equipment.name}, {equipment.department.name}'

class ENGCustomMCF(forms.ModelChoiceField):
    def label_from_instance(self, engineer):
        return f'{engineer.first_name} {engineer.last_name}'

class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        doc_hos = Doctor.objects.get(id = self.request.user.id).current_hospital
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].queryset = doc_hos.equipment_set.filter(status = 'LIVE') 

    class Meta:
        model = Ticket
        fields = ['equipment', 'ticket_type']

    
    
    
    ticket_type = forms.ChoiceField(
        choices=Ticket.types,
        widget = forms.Select
    )

   
    
    equipment = CustomMCF(
        queryset= None, 
        widget = forms.Select
    )


class TicketFormID(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ticket_type', 'status']
    
    
    ticket_type = forms.ChoiceField(
        choices=Ticket.types,
        widget = forms.Select
    )

    status = forms.ChoiceField(
        choices=Ticket.STATUS,
        widget = forms.Select
    )

class AssignEng(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        man = Manager.objects.get(id = self.request.user.id)
        super(AssignEng, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = man.hospital.engineer_set.all()

    class Meta:
        model = Ticket
        fields = ['user']
    
    user = ENGCustomMCF(
        queryset= None, 
        widget = forms.Select
    )

class AddDepartmentForm(forms.ModelForm):
    
    class Meta:
        model = Department
        fields = ['name']
    
    name = forms.CharField(max_length=100)

class AddEquipmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        eng_hos = Engineer.objects.get(id = self.request.user.id).current_hospital
        super(AddEquipmentForm, self).__init__(*args, **kwargs)
        self.fields['department'].queryset = eng_hos.department_set.all() 
    
    class Meta:
        model = Equipment
        fields = ['name', 'specs', 'quantity', 'serial_num', 'department']
    
    name = forms.CharField(max_length=100)
    specs = forms.Textarea()
    quantity = forms.IntegerField()
    serial_num = forms.IntegerField()

    department = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select
    )
     