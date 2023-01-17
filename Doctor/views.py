from django.shortcuts import redirect, render
from Doctor.forms import DoctorProfileForm
from Doctor.models import *
from home.decorators import allow_users
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home.models import Appointment
from Patient.models import *
from datetime import datetime, timedelta,date
from django.contrib.auth.models import User
from django.views.generic import ListView
from Doctor.forms import UserProfileForm
# Create your views here.
@login_required(login_url='login')
@allow_users(allowed_roles='doctor')
def doctorProfile(request):
    if request.method=='GET':
        dp=DoctorProfileForm(instance=request.user.doctor)
        u_f=UserProfileForm(instance=request.user)
        context={'form': dp , 'u_form': u_f}
        return render(request, 'Doctor/doctorProfile.html',context)
    if request.method=='POST':
        form=DoctorProfileForm(request.POST, request.FILES,instance=request.user.doctor)
        u_form=UserProfileForm(request.POST, instance=request.user)
        if form.is_valid() and u_form.is_valid():
            doctorName=form.cleaned_data.get('DoctorName')
            catagory=form.cleaned_data.get('catagory_id')
            pic=form.cleaned_data.get('profilePicture')
            d=Doctor.objects.get(user=request.user)
            d.DoctorName=doctorName
            d.catagory_id=catagory
            d.profilePicture=pic
            d.save()
            u_form.save()
            messages.success(request,"Account Created Successfully")
            return redirect('doctorProfile')
    return render(request,'Doctor/dashboard.html')
@login_required(login_url='login')
@allow_users(allowed_roles='doctor')
def dashboard(request):
    doctor=Doctor.objects.get(user=request.user.id)
    todayApp=Appointment.objects.filter(appointment_date=datetime.today(), doctor_id=doctor, status=True)
    total=todayApp.count()
    dc=DiceaseCatagory.objects.all()
    disCatCouts=[]
    days_before = (date.today()-timedelta(days=30)).isoformat()
    lastMonthAppointmentsCount=Appointment.objects.filter(doctor_id=doctor, appointment_date__gte=days_before).count()
    unTreatedAppointments=Appointment.objects.filter(doctor_id=doctor, appointment_date__gte=days_before, status=True).count()
    totalAppointments=Appointment.objects.filter(doctor_id=doctor).count()
    for c in dc:
        # diceaseCount=Prescription.objects.select_related('doctor_id').filter(diceaseCatagory_id=c.id,prescription_date__gte=days_before).count()
        diceaseCount=Prescription.objects.filter(diceaseCatagory_id=c.id,doctor_id=doctor.id,prescription_date__gte=days_before).count()
        disCatCouts.append(diceaseCount)
    context={'todayApp':todayApp, 'totalTodayAppointments':total, 'diseaseCatagoryCount':disCatCouts, 'diseaseCatagories':dc,'lastMonthAppointmentsCount':lastMonthAppointmentsCount, 'unTreatedAppointments':unTreatedAppointments, 'totalAppointments':totalAppointments}
    return render(request, 'Doctor/dashboard.html',context)
class TodayAppointmentsView(ListView):
    model=Appointment
    context_object_name='todayApps'
    template_name='Doctor/todayAppointments.html'
    paginate_by=5
    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        doctor=Doctor.objects.get(user=self.request.user.id)
        query=qs.filter(appointment_date=datetime.today(), doctor_id=doctor, status=True)
        return query
    
def treatPatient(request, pk):
    if request.method=='GET':
        pc=PatientCondition.objects.get(appointment_id=pk)
        patient_id=pc.patient_id.id
        request.session['patient_id']=patient_id
        dc=DiceaseCatagory.objects.all()
        context={'pc':pc,'dc':dc}
        return render(request,'Doctor/treatPatient.html',context)
    if request.method=='POST':
        diseasCat_id=int(request.POST['diseaseType'])
        diseaseCat=DiceaseCatagory.objects.get(id=diseasCat_id)
        pre=request.POST['pre']
        user_id=request.user.id
        doctor=Doctor.objects.get(user=user_id)
        p_id=request.session.get('patient_id')
        patient=Patient.objects.get(id=p_id)
        app_id=Appointment.objects.get(id=pk)
        presc=Prescription(prescription=pre, patient_id=patient,doctor_id=doctor, appointment_id=app_id, diceaseCatagory_id=diseaseCat)
        presc.save()
        messages.success(request,"Prescription has been sent successfuly")
        app_id.status=False
        app_id.save()
        return redirect('doctorDashboard')
class ListTotalAppointments(ListView):
    model=Appointment
    context_object_name="totalApp"
    template_name='Doctor/totalAppointments.html'
    def get_queryset(self,**kwargs):
        qs=super().get_queryset(**kwargs)
        doctor=Doctor.objects.get(user=self.request.user.id)
        query=qs.filter(doctor_id=doctor)
        return query
class ListMonthlyAppointments(ListView):
    model=Appointment
    context_object_name="monthlyApp"
    template_name='Doctor/monthlyAppointments.html'
    def get_queryset(self,**kwargs):
        qs=super().get_queryset(**kwargs)
        doctor=Doctor.objects.get(user=self.request.user.id)
        days_before = (date.today()-timedelta(days=30)).isoformat()
        query=qs.filter(doctor_id=doctor, appointment_date__gte=days_before)
        return query
class ListExpireAppointments(ListView):
    model=Appointment
    context_object_name="expireApp"
    template_name='Doctor/expireAppointments.html'
    def get_queryset(self,**kwargs):
        qs=super().get_queryset(**kwargs)
        doctor=Doctor.objects.get(user=self.request.user.id)
        days_before = (date.today()-timedelta(days=30)).isoformat()
        query=qs.filter(doctor_id=doctor, appointment_date__gte=days_before,status='True')
        return query