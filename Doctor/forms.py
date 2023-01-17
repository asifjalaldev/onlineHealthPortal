from django import forms
from django.contrib.auth.models import User
from Doctor.models import Doctor
class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model=Doctor
        fields=['profilePicture','DoctorName', 'catagory_id']
class UserProfileForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email']