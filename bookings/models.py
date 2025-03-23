from django.db import models
from django.contrib.auth.models import User

# Модель для номеров
class Room(models.Model):
    number = models.CharField(max_length=10)  # Номер комнаты (например, "101")
    description = models.TextField()  # Описание комнаты
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена за ночь
    photo = models.ImageField(upload_to='room_photos/', null=True, blank=True)  # Фото номера

    def __str__(self):
        return f"Room {self.number}"

# Модель для бронирования
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Связь с номером
    check_in = models.DateField()  # Дата заезда
    check_out = models.DateField()  # Дата выезда
    created_at = models.DateTimeField(auto_now_add=True)  # Время создания бронирования

    def __str__(self):
        return f"Booking by {self.user.username} for Room {self.room.number}"
