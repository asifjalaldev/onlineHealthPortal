import django
from django.db import models
from Patient.models import Patient
from home.models import Appointment
from django.conf import settings
from django.contrib.auth import get_user_model
from PIL import Image
User = get_user_model()
# Create your models here.
class DoctorCatagory(models.Model):
    catagoryName=models.CharField(max_length=100)
    def __str__(self):
        return self.catagoryName
class Doctor(models.Model):
    DoctorName=models.CharField(max_length=100, null=True, default=None)
    catagory_id=models.ForeignKey(DoctorCatagory,on_delete=models.CASCADE, null=True, default=None)
    profilePicture=models.ImageField(default=None, null=True,upload_to='profilePictures')
    user=models.OneToOneField(User,on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.user.username
    def save(self,*args, **kwargs):
        super().save()
        img=Image.open(self.profilePicture.path)
        if img.height > 300 or img.width > 300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.profilePicture.path)

class DiceaseCatagory(models.Model):
      name=models.CharField(max_length=100, blank=True)

class Prescription(models.Model):
    prescription=models.TextField()
    prescription_date=models.DateField(default=django.utils.timezone.now)
    patient_id=models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor_id=models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_id=models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diceaseCatagory_id=models.ForeignKey(DiceaseCatagory, on_delete=models.CASCADE, default=None)