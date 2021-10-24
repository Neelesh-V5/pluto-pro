from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Day)
admin.site.register(Country)
admin.site.register(FoodBank)
admin.site.register(WorkingDays)
admin.site.register(RequestTicket)