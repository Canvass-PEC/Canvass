from django.contrib import admin

# Register your models here.
from .models import Activity,Notification
admin.site.register(Activity)
admin.site.register(Notification)