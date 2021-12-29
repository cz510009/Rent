from django.db import models
 
# Create your models here.
 
 
class Rent(models.Model):
    user = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    url=models.CharField(max_length=300)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    rent = models.CharField(max_length=200)
    layout= models.CharField(max_length=200)
    area = models.CharField(max_length=200)
    station = models.CharField(max_length=200)
    timeOnFoot = models.CharField(max_length=200)
    age = models.CharField(max_length=200)
    difference = models.FloatField()
    bargain = models.BooleanField()
    def __str__(self):
            return self.name