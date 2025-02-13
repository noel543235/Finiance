from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    # Basic information inherited
    date_of_birth = models.DateField(null=True, blank=True)