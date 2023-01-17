from django.contrib import admin
from .models import Patient,PatientCondition
# Register your models here.
admin.site.register(Patient)
admin.site.register(PatientCondition)