from django.db import models
from .engineer import Engineer
from .session import Session

class SessionEngineer(models.Model):
    engineer_id = models.ForeignKey(Engineer, on_delete=models.CASCADE, related_name='engineer_id')
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='session_id')
