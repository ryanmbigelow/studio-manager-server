from django.db import models
from .engineer import Engineer

class Session(models.Model):
    artist = models.CharField(max_length=55)
    date = models.DateField()
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    engineer_id = models.ForeignKey(Engineer, on_delete=models.CASCADE)
