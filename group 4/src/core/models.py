import time
import hashlib
from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)
    unique_id = models.CharField(max_length=6, primary_key=True, blank=True)
    def save(self, *args, **kwargs):
        timestamp = str(int(time.time() * 1000))
        username = self.user.username
        to_hash = timestamp + username
        hashed = hashlib.sha256(to_hash.encode()).hexdigest()
        self.unique_id = ''.join(filter(str.isalnum, hashed))[:6]
        super().save(*args, **kwargs)
