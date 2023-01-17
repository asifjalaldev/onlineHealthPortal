from django.contrib import admin
from django.urls import path,include
from Patient.views import *
from . import views 


urlpatterns = [
    path('dashboard/', views.dashboard, name='patientDashboard'),
    path('patientProfile/', views.patientProfile, name='patientProfile'),
    path('bookAppointment/<int:pk>' , views.bookAppointment, name='bookAppointment'),
    path('delete/<int:pk>' , views.deleteAppointment, name='deleteAppointment'),
    path('patientCondition/', CreatePatientCondition.as_view(), name='createCondition'),
    path('patientCondition/<int:pk>',views.patientConditonDetail,name='patientConditionDetail'),
    path('updatePatientCondition/<int:pk>', UpdatePCondView.as_view(), name='UpdatePC'),
    path('updateAppointment/<int:pk>',EditAppiontmentView.as_view(),name='updateAppointment'),
    path('searchDoctors/', views.searchDoctors, name='searchDoctors'),
    path('PreD/<int:pk>',PrescriptionDetailView.as_view(),name='PrescriptionDetailView'),
      path('AppointmentDetail/<int:pk>',AppointmentDetailView.as_view(),name='AppointmentDetail'),
      path('appointmentDetail/<int:pk>',views.appointmentDetailView,name='appointmentDetailView')
]
