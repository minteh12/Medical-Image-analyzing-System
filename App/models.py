from django.db import models
from datetime import date

class Patient(models.Model):
    name = models.CharField(max_length=100)
    patient_id = models.CharField(max_length=100)
    date = models.DateField(default=date.today)
    medical_image = models.ImageField(upload_to='medical_images/')
    type = models.CharField(max_length=100, default='No Type')
    result = models.CharField(max_length=100, default='No result')
    


    def __str__(self):
        return self.name
