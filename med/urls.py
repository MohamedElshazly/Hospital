from django.urls import path
from med.views import (CreateHospitalView, 
                        HospitalDetailsView, 
                        SearchHospitalResultsView, 
                        SearchHospitalView, 
                        EquipmentListView, 
                        EquipmentDetailsView,
                        NotificationsListView,
                        DepartmentListView, 
                        List_Create_CompanyView, 
                        generate_PDF)

urlpatterns = [
    path('register_hospital/', CreateHospitalView.as_view(), name='register-hospital' ),
    path('search/', SearchHospitalView.as_view(), name ='hospital-search'),
    path('search-results/', SearchHospitalResultsView.as_view(), name ='hospital-search-results'),
    path('equipment-list/', EquipmentListView.as_view(), name ='equipment-list'),
    path('department-list/', DepartmentListView.as_view(), name ='department-list'),
    path('hospital-details/<int:pk>/', HospitalDetailsView.as_view(), name ='hospital-details'),
    path('equipment-details/<int:pk>/', EquipmentDetailsView.as_view(), name ='equipment-details'),
    path('list-notifications/', NotificationsListView.as_view(), name ='list-notifications'),
    path('list-create-company/', List_Create_CompanyView.as_view(), name ='list-create-company'),
    path('get-pdf/<int:pk>/', generate_PDF, name ='get-pdf')
]