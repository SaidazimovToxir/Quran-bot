from typing import Any
from django.db import models

# Create your models here.

class BotUser(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, null=True, blank=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return str(self.name)
    
    
class Feedback(models.Model):
    name = models.CharField(max_length=200)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self) -> str:
        return str(self.name)