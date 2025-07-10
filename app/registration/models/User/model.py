from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (
        ('student', 'Ученик'),
        ('trainer', 'Тренер'),
        ('manager', 'Руководитель'),
        ('admin', 'Администратор'),
    )
    
    role = models.CharField(max_length=10, choices=ROLES, null=False)
    phone = models.CharField(max_length=20, null=True, blank=True)
    birth_date = models.DateField(null=True)
    city = models.CharField(max_length=100)
    parent_name = models.CharField(max_length=100)
    parent_phone = models.CharField(max_length=20)
    rank = models.CharField(max_length=50)
    rank_date = models.DateField(null=True)
    email = models.EmailField(default=None)
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"