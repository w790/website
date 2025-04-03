from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/',views.home_view, name='home'),
    path('create_booking/', views.create_booking, name='create_booking'),
    path('booking_success/', views.booking_success, name='booking_success'),
    path('room_list/', views.room_list, name='room_list'),
    path('add_room/', views.add_room, name='add_room'),
]