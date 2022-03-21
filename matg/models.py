from django.db import models

class Registration(models.Model):
    name=models.CharField(max_length=100)
    phone=models.IntegerField()
    email=models.EmailField(primary_key=True)
    password=models.CharField(max_length=100)
    is_active=models.BooleanField()
class Course(models.Model):
    courseimage=models.CharField(max_length=100000000)
    coursetitle=models.CharField(max_length=20000)
    aboutcourse=models.CharField(max_length=100000)
    price=models.CharField(max_length=20)
