from django.urls import path
from med.views import (CreateHospitalView, 
                        HospitalDetailsView, 
                        SearchHospitalResultsView, 
                        SearchHospitalView, 
                        EquipmentListView, 
                        EquipmentDetailsView, 
                        generate_PDF)

urlpatterns = [
    path('register_hospital/', CreateHospitalView.as_view(), name='register-hospital' ),
    path('search/', SearchHospitalView.as_view(), name ='hospital-search'),
    path('search-results/', SearchHospitalResultsView.as_view(), name ='hospital-search-results'),
    path('equipment-list/', EquipmentListView.as_view(), name ='equipment-list'),
    path('hospital-details/<int:pk>/', HospitalDetailsView.as_view(), name ='hospital-details'),
    path('equipment-details/<int:pk>/', EquipmentDetailsView.as_view(), name ='equipment-details'),
    path('get-pdf/<int:pk>/', generate_PDF, name ='get-pdf')
]