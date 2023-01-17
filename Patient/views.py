from django.shortcuts import render,redirect
from django.urls import reverse, reverse_lazy
from Doctor.models import Doctor,DoctorCatagory
from Patient.forms import patientUpdateForm,userProfileForm
from Patient.models import Patient, PatientCondition
from django.contrib.auth.decorators import login_required
from home.decorators import allow_users
from django.contrib import messages
from django.views.generic import CreateView,UpdateView
from home.models import Appointment
from Patient.forms import BookAppointmentForm
from django.contrib.auth.models import User
from Doctor.models import *
from django.db.models import Q
from django.views.generic import *
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
# Create your views here.
@login_required(login_url='login')
@allow_users(allowed_roles=['patient'])
def dashboard(request):
    if request.method=="GET":
        current_date=datetime.now().date()
        doctors=Doctor.objects.all()
        user=User.objects.get(id=request.user.id)
        p=Patient.objects.get(user=user)
        apps=Appointment.objects.filter(patient_id=p,status=True, appointment_date__gte=current_date)
        paginator = Paginator(doctors,4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        total=10
        availableSlotsDict={}
        # myapp=Appointment.objects.filter(patient_id=request.user)
        for doctor in doctors:
            appointments=Appointment.objects.filter(doctor_id=doctor, appointment_date=current_date).count()
            doctorUsername=doctor.user.username
            availableSlots=total-appointments
            availableSlotsDict[doctor.id]=availableSlots
        print(availableSlotsDict)
        doctorsCatagories=DoctorCatagory.objects.all()
        prescriptions=Prescription.objects.filter(patient_id=p).order_by('-appointment_id')[:2]#getting the lattest two presc data 
        context={'page_obj':page_obj,'slotsDict':availableSlotsDict, 'apps': apps, 'cdate': current_date, 'docCat':doctorsCatagories, 'pre':prescriptions}
        return render(request, 'Patient/dashboard.html',context)

class myAppointments(LoginRequiredMixin,ListView):
    model=Appointment
    context_object_name='myApps'
    template_name='Patient/myAppointments.html'
    def get_queryset(self, **kwargs):
        qs=super().get_queryset(**kwargs)
        apps=qs.filter(patient_id=self.request.user.patient)
        return apps

@login_required(login_url='login')
@allow_users(allowed_roles=['patient'])
def patientProfile(request):
    if request.method=='GET':
            u_f=userProfileForm(instance=request.user)
            pu_f=patientUpdateForm(instance=request.user.patient)
            context={'form': pu_f, 'u_f':u_f}
            return render(request, 'Patient/patientProfile.html',context)
    if request.method=='POST':
        form=patientUpdateForm(request.POST,  request.FILES, 
                                    instance=request.user.patient)
        u_f=userProfileForm(request.POST,instance=request.user)
        if form.is_valid() and u_f.is_valid():
            u_f.save()
            patientName=form.cleaned_data.get('patientName')
            DOB=form.cleaned_data.get('DOB')
            imag_url=form.cleaned_data.get('profilePicture')
            d=Patient.objects.get(user=request.user)
            d.patientName=patientName
            d.DOB=DOB
            d.profilePicture=imag_url
            d.save()
            messages.success(request,"Your Profile Updated Successfully")
            return redirect('patientProfile')
        else:
            print('form not valid')
    return render(request,'patient/dashboard.html')
@login_required(login_url='login')
@allow_users(allowed_roles=['patient'])
def bookAppointment(request,pk):
    if request.method=='GET':
        form= BookAppointmentForm
        current_date=datetime.now().date()
        doctor=Doctor.objects.get(id=pk)
        Num_of_appointments=Appointment.objects.filter(doctor_id=doctor, appointment_date=current_date).count()
        total=10
        avalaibleSlots=total-Num_of_appointments
        context={'form': form, 'avalaibleSlots':avalaibleSlots,'doctor':doctor}
        return render(request,'home/appointment_form.html',context)
    if request.method=='POST':
        form=BookAppointmentForm(request.POST) 
        if form.is_valid():
            input_time=form.cleaned_data.get('time')
            date=form.cleaned_data.get('appointment_date')
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            cinput_time=input_time.strftime("%H:%M:%S")
            doctor=Doctor.objects.get(id=pk)
            user=User.objects.get(id=request.user.id)
            patient=Patient.objects.get(user=user)
            apps=Appointment.objects.filter(appointment_date=date, time=input_time,doctor_id=doctor)
            if apps:
                messages.error(request,"Sorry, this date and time has already selected, choose another one.")
                form= BookAppointmentForm
                context={'form': form}
                return render(request, 'home/appointment_form.html',context)
            elif datetime.today().date() > date : 
                messages.error(request,f"Sorry, selected date {date} is already expired! ")
                form= BookAppointmentForm
                context={'form': form}
                return render(request, 'home/appointment_form.html',context)
            elif Appointment.objects.filter(appointment_date=date,doctor_id=doctor, patient_id=patient, status=True):
                messages.error(request,f"You already have an appointment on {date}.")
                form= BookAppointmentForm
                context={'form': form}
                return render(request, 'home/appointment_form.html',context)
            elif len(Appointment.objects.filter(appointment_date=date, doctor_id=doctor))>=10:
                messages.error(request,f"{doctor.DoctorName} slote for {date} filled, choose another date.")
                form= BookAppointmentForm
                context={'form': form}
                return render(request, 'home/appointment_form.html',context)
            elif current_time > cinput_time and  datetime.today() == date:
                messages.error(request,f"{date} or {input_time} already expired.")
                form= BookAppointmentForm
                context={'form': form}
                return render(request, 'home/appointment_form.html',context)
            else:
                user=User.objects.get(id=request.user.id)
                patient=Patient.objects.get(user=user)
                app=Appointment(appointment_date=date, time=input_time, patient_id=patient,doctor_id=doctor)
                app.save()
                request.session['appoinment_id']=app.id
                messages.success(request,"Your appoinment has been booked!")
                return redirect('createCondition')
@login_required(login_url='login')
@allow_users(allowed_roles=['patient'])   
def deleteAppointment(request,pk):
    app=Appointment.objects.get(id=pk)
    app.delete()
    messages.success(request,"appoinment has been canceled!")
    return redirect('patientDashboard')
class CreatePatientCondition(LoginRequiredMixin,CreateView):
    model=PatientCondition
    template_name="Patient/patientCondition.html"
    success_url=reverse_lazy('patientDashboard')
    error_message="something went wrong."
    fields=['symptoms', 'BP','BMI','BS','HB','platelets']
    def form_valid(self, form ):
        p=Patient.objects.get(user=self.request.user) #getting patient
        app_id=self.request.session.get('appoinment_id')#getting appointment id from session in book appointment method
        app=Appointment.objects.get(id=app_id) #getting appoinement object of curent appointment
        form.instance.appointment_id=app #put the appoinement_id data in form.instance.appoinemtn_id  
        form.instance.patient_id = p#storing patient data in the form
        messages.success(self.request, "You appointment has been booked. Doctor review your symtoms very soon.")
        return super().form_valid(form) 
@login_required(login_url='login')
@allow_users(allowed_roles=['patient'])
def patientConditonDetail(request, pk):
   if request.method=='GET':
    
            pc=PatientCondition.objects.get(appointment_id=pk)
            request.session['app_id']=pk
            context={'pc':pc}
            return render(request,'Patient/patientConditionDetail.html',context)
class UpdatePCondView(LoginRequiredMixin,UpdateView):
    model=PatientCondition
    fields=['symptoms','BP','BMI', 'BS', 'HB','platelets']
    def get_success_url(self):
        pc_id=self.kwargs['pk']
        pc=PatientCondition.objects.get(id=pc_id)
        return reverse('appointmentDetailView', kwargs={'pk': pc.appointment_id.id})
    def form_valid(self, form):
        user=User.objects.get(id=self.request.user.id)
        form.instance.patient_id=Patient.objects.get(user=user)
        form.instance.appointment_id=Appointment.objects.get(id=self.request.session.get('app_id'))
        return super().form_valid(form)
class EditAppiontmentView(LoginRequiredMixin,UpdateView):
    model=Appointment
    form_class=BookAppointmentForm
    success_url=reverse_lazy('patientDashboard')
    def form_valid(self, form):
            input_time=form.cleaned_data.get('time')
            date=form.cleaned_data.get('appointment_date')
            now = datetime.datetime.now()
            current_time = now.strftime("%H:%M:%S")
            cinput_time=input_time.strftime("%H:%M:%S")
            pk=self.kwargs['pk']
            app=Appointment.objects.get(id=pk)
            doctor=app.doctor_id
            user=User.objects.get(id=self.request.user.id)
            patient=Patient.objects.get(user=user)
            apps=Appointment.objects.filter(appointment_date=date, time=input_time,doctor_id=doctor)
            if apps:
                messages.error(self.request,"Sorry, this date and time has already selected, choose another one.")
                form= BookAppointmentForm
                context={'form': form}
                return render(self.request, 'home/appointment_form.html',context)
            elif datetime.date.today() > date : 
                messages.error(self.request,f"Sorry, selected date {date} is already expired! ")
                form= BookAppointmentForm
                context={'form': form}
                return render(self.request, 'home/appointment_form.html',context)
            elif Appointment.objects.filter(appointment_date=date,doctor_id=doctor, patient_id=patient):
                messages.error(self.request,f"You already have an appointment on {date}.")
                form= BookAppointmentForm
                context={'form': form}
                return render(self.request, 'home/appointment_form.html',context)
            elif len(Appointment.objects.filter(appointment_date=date, doctor_id=doctor))>=10:
                messages.error(self.request,f"{doctor.DoctorName} slote for {date} filled, choose another date.")
                form= BookAppointmentForm
                context={'form': form}
                return render(self.request, 'home/appointment_form.html',context)
            elif current_time > cinput_time and  datetime.date.today() == date:
                messages.error(self.request,f"{date} or {input_time} already expired.")
                form= BookAppointmentForm
                context={'form': form}
                return render(self.request, 'home/appointment_form.html',context)
            else:
                user=User.objects.get(id=self.request.user.id)
                patient=Patient.objects.get(user=user)
                app=Appointment(id=pk, appointment_date=date, time=input_time, patient_id=patient,doctor_id=doctor)
                app.save()
                self.request.session['appoinment_id']=app.id
                messages.success(self.request,"Your appoinment has been updated!")
                return super().form_valid(form)

def searchDoctors(request):
   
    if request.method=='GET':
        doctorsCatagories=DoctorCatagory.objects.all()
        doctors=Doctor.objects.all()
        total=doctors.count()
        query=request.GET.get('query')
        catagory=request.GET.get('catagory')
        paginator = Paginator(doctors,12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        if query is None and catagory is None:
            context={'page_obj': page_obj, 'docCat':doctorsCatagories, 'total': total}
            return render(request, 'Patient/searchDoctors.html', context)
        if int(catagory)==0:
                doctors=Doctor.objects.filter(Q(DoctorName__icontains=query))
                paginator = Paginator(doctors,12)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                total=len(doctors)
                context={'page_obj':page_obj, 'docCat': doctorsCatagories, 'total':total}
                return render(request, 'Patient/searchDoctors.html',context)
            # filter(A, B) is the AND while   filter(A).filter(B) is OR         
        else:
                doctors=Doctor.objects.filter(Q(DoctorName__icontains=query)).filter( Q(catagory_id=catagory))
                total=doctors.count()
                paginator = Paginator(doctors,12)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
        context={'page_obj':page_obj, 'docCat': doctorsCatagories, 'total':total}
        return render(request, 'Patient/searchDoctors.html',context)
class PrescriptionDetailView(LoginRequiredMixin,DetailView):
    model=Prescription
    template_name='Patient/PrescriptionDetail.html'
    context_object_name='pre'
class AppointmentDetailView(DetailView):
    model=Appointment
    template_name="Patient/AppointmentDetail.html"
    context_object_name='app'
@login_required(login_url='login')
@allow_users(allowed_roles=['patient'])
def appointmentDetailView(request,pk):
    if request.method=='GET':
        app=Appointment.objects.get(id=pk)
        pc=PatientCondition.objects.get(appointment_id=pk)
        print(pc)
        request.session['app_id']=pk
        context={'app': app, 'pc':pc}
        return render(request,'Patient/appointmentDetail.html',context)