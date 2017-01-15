from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=30)
    version = models.CharField(max_length=10)
    created_time = models.DateField(auto_now_add=True)

class Data(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='related_data')
    command = models.CharField(max_length=30)
    data = models.TextField()
    created_time = models.DateField(auto_now_add=True)
