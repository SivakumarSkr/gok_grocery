from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    pass


class Voluteer(User):
    pass


class Area(models.Model):
    name = models.CharField(max_length=100, blank=False)
    centre = models.TextField(blank=False)
    # head = models.OneToOneField(User)