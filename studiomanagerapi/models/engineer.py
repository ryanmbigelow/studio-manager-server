from django.db import models

class Engineer(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    is_admin = models.BooleanField()
    profile_picture = models.CharField(max_length=55)
    uid = models.CharField(max_length=55)
