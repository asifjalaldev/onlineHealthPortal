from django.shortcuts import redirect, render
from account.forms import SignUpForm
from Patient.models import Patient
from Doctor.models import Doctor
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.

def register(request):
    if request.method=='POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            roleField=form.cleaned_data.get('roleField')
            user=form.save()
            if int(roleField)==2:
                p=Patient(user=form.instance)
                p.save()
                group=Group.objects.get(name='patient')
                user.groups.add(group)
                return redirect('login')
            if int(roleField)==3:
                d=Doctor(user=form.instance)
                d.save()
                group=Group.objects.get(name='doctor')
                user.groups.add(group)
                return redirect('login')
    
    if request.method=='GET':
        form=SignUpForm()
    context={'form':form}
    return render(request,'account/register.html',context)   
    # def form_valid(self, form):

   