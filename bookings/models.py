from django.db import models
from django.contrib.auth.models import User

# Модель для номеров
class Room(models.Model):
    number = models.CharField(max_length=10)  # Номер комнаты (например, "101")
    description = models.TextField()  # Описание комнаты
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена за ночь
    photo = models.ImageField(upload_to='room_photos/')  # Фото номера

    def __str__(self):
        return f"Room {self.number}"

# Модель для бронирования
class Booking(models.Model):
    STATUS_CHOICES = [
        ("Ожидание", "Ожидание"),
        ("Подтверждено", "Подтверждено"),
        ("Отменено", "Отменено"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="Пользователь")  # Связь с пользователем
    room = models.ForeignKey(Room, on_delete=models.CASCADE,verbose_name="Комната")  # Связь с номером
    check_in = models.DateField(verbose_name="Дата заселения")  # Дата заезда
    check_out = models.DateField(verbose_name="Дата выселения")  # Дата выезда
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Дата бронирования со временем")  # Время создания бронирования
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Ожидание")

    def __str__(self):
        return f"{self.user.username} забронировал комнату {self.room} с {self.check_in} по {self.check_out}"
    def is_available(self):
        # Проверяет, доступен ли номер для выбранных дат.
        existing_bookings = Booking.objects.filter(room=self.room)#objects-менеджер модели, предоставляющий интерфейс для работы с базой данных
        #.filter(room=self.room)-Метод фильтрации, который возвращает QuerySet (набор объектов)
        #Фильтрует записи в таблице Booking, где поле room равно текущей комнате (self.room)
        #В SQL это соответствует:SELECT * FROM bookings_booking WHERE room_id = {self.room.id};

        #QuerySet "ленивый" - запрос к БД выполняется только при итерации или вызове методов
        #(получается тут мы обратились к базе данных вытащили все бронирования комнаты id которой равно id текущей комнаты)
        for booking in existing_bookings:
            if (self.check_in < booking.check_out and self.check_out > booking.check_in):
                return False
        return True