from django.db import models
from django.contrib.auth.models import User

class EnergyUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=False)
    usage_value = models.FloatField()
    irms_current = models.FloatField()  
    irms_power = models.FloatField() 
    peak_power = models.FloatField()  

