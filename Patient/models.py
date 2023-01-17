import datetime
from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image
User = get_user_model()
# Create your models here.
class Patient(models.Model):
    patientName=models.CharField(max_length=50, null=True, default=None)
    DOB=models.DateField( null=True, default=None)
    profilePicture=models.ImageField(default=None, null=True,upload_to='profilePictures')
    user=models.OneToOneField(User,on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.patientName
    def save(self,*args, **kwargs):
        super().save()
        img=Image.open(self.profilePicture.path)
        if img.height > 300 or img.width > 300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.profilePicture.path)
class PatientCondition(models.Model):
    symptoms=models.TextField()
    BP=models.CharField(max_length=50,blank=True)
    BMI=models.CharField(max_length=50,blank=True)
    BS=models.CharField(max_length=50,blank=True)
    HB=models.CharField(max_length=50,blank=True)
    platelets=models.CharField(max_length=50,blank=True)
    patient_id=models.ForeignKey(Patient,on_delete=models.CASCADE)
    appointment_id=models.ForeignKey("home.Appointment",on_delete=models.CASCADE)
    
class TestReport(models.Model):
    report_path=models.CharField(max_length=100)
    prescription_id=models.ForeignKey("Doctor.Prescription", on_delete=models.CASCADE)