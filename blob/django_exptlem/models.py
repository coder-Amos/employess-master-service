from django.db import models


# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    department = models.CharField(max_length=30,null=True)
    tel = models.CharField(max_length=20,null=True)
    isworking = models.BooleanField(default=True)
