from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PendingActionable(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.CharField(max_length=100)
    clientRemarks = models.CharField(max_length=500, blank=True)
    status = models.BooleanField(default=False, blank=True)
    # attachedDoc = models.FileField()

class WatchOutPoint(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.CharField(max_length=100)