from django import forms
from Patient.models import Patient, PatientCondition
from home.models import Appointment
from django.contrib.auth.models import User
class DateInput(forms.DateInput):
    input_type='date'
class TimeInput(forms.TimeInput):
    input_type='time'
class patientUpdateForm(forms.ModelForm):
    DOB=forms.DateField(widget=DateInput)
    class Meta:
        model=Patient
        fields=['profilePicture','patientName', 'DOB']
class userProfileForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email']
class BookAppointmentForm(forms.ModelForm):
    appointment_date=forms.DateField(widget=DateInput)
    time=forms.TimeField(widget= TimeInput)
    class Meta:
        model=Appointment
        fields=['appointment_date', 'time']
class PatientCondDetailForm(forms.ModelForm):
    class Meta:
        model=PatientCondition
        fields=['symptoms','BP', 'BMI', 'BS','HB','platelets']

        