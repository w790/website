from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test,login_required
from .forms import CustomUserCreationForm,CustomAuthenticationForm, RoomForm, BookingForm
from .models import Booking,Room,Notification
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import get_user_model


User = get_user_model()

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
        form = CustomAuthenticationForm(data=request.POST)
        print("Form errors:", form.errors)  # Добавьте эту строку
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу
    else:
        form = CustomAuthenticationForm()
    return render(request, 'bookings/login.html', {'form': form})

def logout_view(request):#Выхода пользователя из системы
    logout(request)
    return redirect('login')

def home_view(request):
    rooms = Room.objects.all()
    return render(request,'bookings/home.html',{'rooms': rooms})

def admin_check(user):
    return user.is_staff

@login_required
@user_passes_test(admin_check)
def room_list(request):
    rooms = Room.objects.all()
    return render(request,'bookings/room_list.html',{'rooms': rooms})

# Добавление номера
@login_required
@user_passes_test(admin_check)
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'bookings/add_room.html', {'form': form})


# Удаление номера
@login_required
@user_passes_test(admin_check)
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    room.delete()
    return redirect('room_list')

#Представление для редактирования номера
@login_required
@user_passes_test(admin_check)
def room_edit(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room)#instance=room — говорит Django: «Мы редактируем существующую комнату, а не создаём новую».
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'bookings/room_form.html', {'form': form})

#представление для создания бронирования
@login_required
def create_booking(request):
    print("Текущий пользователь:", request.user)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # Устанавливаем текущего пользователя
            print("Перед сохранением: ", booking.user, booking.room, booking.check_in, booking.check_out)
            booking.save()
            return redirect('booking_success')  # Переход к успешному бронированию
    else:
        form = BookingForm()

    return render(request, 'bookings/create_booking.html', {'form': form})


#представление для успешного бронирования
@login_required
def booking_success(request):
    return render(request,'bookings/booking_success.html')


#user представление для отмены бронирований если бронирование находиться в ожидании
@login_required
def user_cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status == "Ожидание":
        booking.delete()
        messages.success(request, "Бронирование успешно отменено")
    else:
        # Добавляем сообщение, если бронирование нельзя отменить
        messages.error(request, "Невозможно отменить бронирование с текущим статусом")

    return redirect("user_dashboard")

@login_required
def user_dashboard(request):
    bookings = Booking.objects.filter(user=request.user)  # Получаем бронирования текущего пользователя
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')[:5]  # Последние 5 непрочитанных

    return render(request, 'bookings/user_dashboard.html', {
        'bookings': bookings,
        'notifications': notifications
    })



@login_required
@user_passes_test(admin_check)
def booking_list(request):
    bookings = Booking.objects.all()  # Получаем все бронирования
    return render(request, "bookings/booking_list.html", {"bookings": bookings})


#admin представление для подтверждения бронирования
@login_required
@user_passes_test(admin_check)
def confirm_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = "Подтверждено"
    booking.save()
    return redirect("booking_list")#администратор после подтверждения бронирования всегда возвращается на свежую страницу списка бронирований, что может дать ему больше уверенности в актуальности данных.


#admin представление для отмены бронирования
@login_required
@user_passes_test(admin_check)
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    #добавить логику отмены бронирования тут нужно создать уведомление что отменено
    Notification.objects.create(
        user=booking.user,
        message =f"Администратор отменил бронирование комнаты {booking.room.number} c {booking.check_in} по {booking.check_out}",
        booking_id=booking.id,
    )
    booking.delete()
    messages.success(request, "Бронирование отменено, пользователь уведомлен")
    return redirect("booking_list")

# views.py
@login_required
def mark_notifications_read(request):
    if request.method == "POST":
        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})