from django.contrib import admin
from django.urls import path,include
from Doctor.views import *
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard,name='doctorDashboard'),
    path('doctorProfile/', views.doctorProfile, name='doctorProfile'),
    path('treatPatient/<int:pk>', views.treatPatient, name='treat'),
    path('TodayAppointmentsView/',TodayAppointmentsView.as_view(), name='appointments'),
    path('TotalAppointments/',ListTotalAppointments.as_view(), name='totalAppointments'),
    path('monthlyAppointments/',ListMonthlyAppointments.as_view(), name='monthlyAppointments'),
       path('expireAppointments/',ListExpireAppointments.as_view(), name='expireAppointments'),
]
