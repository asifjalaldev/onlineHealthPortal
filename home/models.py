from django.db import models

# Create your models here.

class Appointment(models.Model):
    appointment_date=models.DateField()
    time=models.TimeField(verbose_name='Time', default=None)
    patient_id=models.ForeignKey("Patient.Patient",on_delete=models.CASCADE)
    doctor_id=models.ForeignKey("Doctor.Doctor", on_delete=models.CASCADE)
    status=models.BooleanField(default=True)