from django.urls import path
from .views import (
                    Submit_Ticket, 
                    List_Tickets, 
                    Submit_Ticket_Using_Id, 
                    Assign_Engineer, 
                    Engineer_Work, 
                    List_Employees,
                    Work_Process,
                    Ticket_Details)

urlpatterns = [
    path('submit-ticket/', Submit_Ticket.as_view(), name='submit-ticket'),
    path('submit-ticket-id/<int:pk>/', Submit_Ticket_Using_Id.as_view(), name='submit-ticket-id'),
    path('ticket-details/<int:pk>/', Ticket_Details.as_view(), name='ticket-details'),
    path('list-tickets/', List_Tickets.as_view(), name = 'list-tickets'),
    path('assign-engineer/<int:pk>/', Assign_Engineer.as_view(), name = 'assign-engineer'),
    path('engineer_work/', Engineer_Work.as_view(), name = 'eng-work'),
    path('list-employees/', List_Employees.as_view(), name = 'list-employees'),
    path('work-process/<int:pk>/<int:pk2>', Work_Process, name='work-process')
]