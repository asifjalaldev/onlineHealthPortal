from django.contrib import admin
from Doctor.models import *
# Register your models here.
admin.site.register(Doctor)
admin.site.register(DoctorCatagory)
admin.site.register(DiceaseCatagory)
admin.site.register(Prescription)