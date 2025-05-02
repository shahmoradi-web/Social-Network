from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    data_of_brith = models.DateField(verbose_name='تاریخ تولد', blank=True, null=True)
    bio = models.TextField(blank=True, null=True, verbose_name='بیوگرافی')
    photo = models.ImageField(upload_to='account_images/',
                              verbose_name='تصویر', default='download.jpg')
    job = models.CharField(max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
