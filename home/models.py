from django.db import models

# Create your models here.
class PendingActionables(models.Model):
    point = models.CharField(max_length=100)

class WatchOut(models.Model):
    point = models.CharField(max_length=100)