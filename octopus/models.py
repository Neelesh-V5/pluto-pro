from django.db import models
from django.contrib.auth.models import AbstractUser
import hashlib
import datetime
import os

def random_gen():
    return hashlib.sha256(str(datetime.datetime.now()).encode()).hexdigest()

def file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (hashlib.sha256(str(datetime.datetime.now()).encode()).hexdigest(), ext)
    return os.path.join("pic/", filename)

# Create your models here.
class User(AbstractUser):
    profile_pic = models.ImageField(null=False, upload_to = file_name)
    Birthday = models.DateField(null=False, blank=False)
    representative = models.BooleanField(null=False)

class Day(models.Model):
    day = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.day}"

class Country(models.Model):
    country_name = models.CharField(max_length=100)
    country_short = models.CharField(max_length=10)
    country_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.country_name}"
    
class FoodBank(models.Model):
    name = models.CharField(null=False, blank=False, max_length=256, unique=True)
    logo = models.ImageField(null=False, upload_to = file_name)
    creator = models.ForeignKey("User", on_delete=models.CASCADE)
    about = models.TextField(null=False, blank=False, max_length=1024)
    opening_time = models.TimeField(null=False, blank=False)
    closing_time = models.TimeField(null=False, blank=False)
    building_number_name = models.CharField(null=False, max_length=25)
    building_street = models.CharField(null=False, max_length= 512)
    building_city = models.CharField(null=False, max_length= 512)
    building_state = models.CharField(null=False, max_length= 512)
    building_pincode = models.CharField(max_length=10,null=False)
    created_on = models.DateTimeField(auto_now_add=True, null=False)
    edited_on = models.DateTimeField(auto_now= True, null=True)
    email = models.EmailField(null=False, blank=False)
    phone_number = models.CharField(max_length=100, null=False, blank=False)
    
    def __str__(self):
        return f"{self.name}"

class WorkingDays(models.Model):
    food_bank = models.ForeignKey("FoodBank", on_delete=models.CASCADE)
    day = models.ForeignKey("Day", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.food_bank} open on {self.day}"

# class FoodBankStorage(models.Model):
#     food_name = models.CharField(null=False, blank=False, max_length=512)
#     food_bank = models.ForeignKey("FoodBank", on_delete=models.CASCADE)
#     food_packages = models.PositiveBigIntegerField(null=False, blank=False)
#     note = models.TextField(null=False, blank=False, max_length=1024)

class RequestTicket(models.Model):
    requested_by = models.ForeignKey("User", on_delete=models.CASCADE)
    requested_on = models.DateTimeField(auto_now_add=True)
    requested_to = models.ForeignKey("FoodBank", on_delete=models.CASCADE)
    pickup_date = models.DateField(null=False, blank=False)
    pickup_time = models.TimeField(null=False, blank=False)
    requested_packages = models.PositiveBigIntegerField(null=False, blank=False)
    note = models.TextField(null=True, max_length=1024)
    completed = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f"Ticket #{self.id} {self.requested_to} {self.pickup_date}"
    

