from django.db import models

# Create your models here.


class Prediction_table(models.Model):
    age = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    education_level = models.CharField(max_length=50)
    occupation = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=50)
    income = models.CharField(max_length=50)
    credit_score = models.CharField(max_length=100)
    status = models.CharField(max_length=100)


