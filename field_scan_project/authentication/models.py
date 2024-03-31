from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.CharField(max_length=255, blank=None)
    faculty = models.CharField(max_length=255, blank=None)
    roles = models.ManyToManyField(Role)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
