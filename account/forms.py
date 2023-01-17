from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
role=(
        ('1', '-- Select --'),
        ('2', 'Patient'),
        ('3', 'Doctor')
    )
class SignUpForm(UserCreationForm):
    roleField=forms.ChoiceField(choices=role, label = ("Role"))
    def clean_roleField(self):
        data=self.cleaned_data.get('roleField')
        if int(data)==1:
            raise forms.ValidationError("Please Select the Role")
        return data
    class Meta:
            model=User
            fields = ['username', 'email','password1', 'password2', 'roleField']

