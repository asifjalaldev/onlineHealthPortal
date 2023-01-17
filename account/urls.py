from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView

from account import views
urlpatterns = [
    # path('register/', Register.as_view(),name='register'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name= 'account/logout.html'), name='logout'),
   
    
]
