from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class User_table(models.Model):
    LOGIN = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    status = models.CharField(max_length=100,default='pending')

class Prediction_table(models.Model):
    User = models.ForeignKey(User_table,on_delete=models.CASCADE)
    ph = models.CharField(max_length=100)
    tds = models.CharField(max_length=100)
    turbidity = models.CharField(max_length=100)
    water_quality = models.CharField(max_length=100)
    explanation = models.CharField(max_length=100)
class Complaints(models.Model):
    User = models.ForeignKey(User_table,on_delete=models.CASCADE)
    complaint = models.CharField(max_length=100)
    reply = models.CharField(max_length=100,default='pending')

class Feedback_table(models.Model):
    User = models.ForeignKey(User_table,on_delete=models.CASCADE)
    feedback = models.CharField(max_length=100)

