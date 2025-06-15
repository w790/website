from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view, name='home'),
    path('booking/create/', views.create_booking, name='create_booking'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.add_room, name='add_room'),
    path('rooms/edit/<int:pk>/', views.room_edit, name='room_edit'),
    path('rooms/delete/<int:pk>/', views.room_delete, name='room_delete'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('bookings/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('bookings/confirm/<int:pk>/', views.confirm_booking, name='confirm_booking'),
    path('bookings/cancel/<int:pk>/', views.cancel_booking, name='cancel_booking'),
    path("booking/user_cancel/<int:pk>/", views.user_cancel_booking, name="user_cancel_booking"),
    path('mark-notifications-read/', views.mark_notifications_read, name='mark_notifications_read'),
]