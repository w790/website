from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, RoomForm, BookingForm
from .models import Booking,Room
from datetime import timedelta

# Представление для страницы регистрации
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу
    else:
        form = CustomUserCreationForm()
    return render(request, 'bookings/register.html', {'form': form})

# Представление для страницы входа
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу
    else:
        form = AuthenticationForm()
    return render(request, 'bookings/login.html', {'form': form})
def home_view(request):
    return render(request,'bookings/home.html')
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'bookings/add_room.html', {'form': form})

def create_booking(request):
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user

            if booking.is_available():
                booking.save()
                return redirect('booking_success')
            else:
                form.add_error('room', 'Этот номер уже забронирован на выбранные даты.')

    else:
        form = BookingForm()

    available_rooms = Room.objects.all()

    if check_in and check_out:
        available_rooms = available_rooms.exclude(
            booking__check_in__lt=check_out,
            booking__check_out__gt=check_in
        )

    # Получаем доступные даты для каждой комнаты
    available_rooms_dates = {}
    for room in available_rooms:
        bookings = Booking.objects.filter(room=room)
        available_dates = []
        for i in range(30):  # Пример для 30 дней
            date = check_in + timedelta(days=i)
            if all(b.check_in > date or b.check_out < date for b in bookings):
                available_dates.append(date)
        available_rooms_dates[room] = available_dates

    return render(request, 'bookings/create_booking.html', {
        'form': form,
        'available_rooms': available_rooms,
        'available_rooms_dates': available_rooms_dates,
        'check_in': check_in,
        'check_out': check_out,
    })

def room_list(request):
    rooms = Room.objects.all()
    return render(request,'bookings/room_list.html',{'rooms': rooms})

def booking_success(request):
    return render(request,'bookings/booking_success.html')
