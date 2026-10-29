from django.db import models

# Create your models here.
#
class Prediction_table(models.Model):
    pregnancies = models.CharField(max_length=100)
    glucose = models.CharField(max_length=100)
    bloodPressure = models.CharField(max_length=100)
    skinThickness = models.CharField(max_length=100)
    insulin = models.CharField(max_length=100)
    bMI = models.CharField(max_length=100)
    diabetesPedigreeFunction = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    outcome = models.CharField(max_length=100)
    explanation = models.CharField(max_length=1000)
