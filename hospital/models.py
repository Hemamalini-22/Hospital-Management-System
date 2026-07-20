from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    doctor_id = models.CharField(max_length=20,unique=True)
    doctor_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.doctor_name

class Patient(models.Model):
    patient_id = models.CharField(max_length=20,unique=True)
    patient_name = models.CharField(max_length=100)
    age = models.IntegerField()
    disease = models.CharField(max_length=100)

    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.patient_name
    
