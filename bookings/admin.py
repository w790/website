from django.contrib import admin
from .models import Room, Booking, CustomUser,Notification

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(CustomUser)
admin.site.register(Notification)