from django.contrib import admin
from home.models import PendingActionable, WatchOutPoint

# Register your models here.
admin.site.register(PendingActionable)
admin.site.register(WatchOutPoint)