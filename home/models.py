from django.db import models

# Create your models here.
class PendingActionable(models.Model):
    point = models.CharField(max_length=100)
    clientRemarks = models.CharField(max_length=500, blank=True)
    status = models.BooleanField(default=False, blank=True)
    # attachedDoc = models.FileField()

class WatchOutPoint(models.Model):
    point = models.CharField(max_length=100)