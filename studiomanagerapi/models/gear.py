from django.db import models
from .category import Category
from .engineer import Engineer

class Gear(models.Model):
    model = models.CharField(max_length=55)
    brand = models.CharField(max_length=55)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    engineer_id = models.ForeignKey(Engineer, on_delete=models.CASCADE, default=0)
