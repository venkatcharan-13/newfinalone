from django.contrib import admin
from home.models import PendingActionables, WatchOut

# Register your models here.
admin.site.register(PendingActionables)
admin.site.register(WatchOut)