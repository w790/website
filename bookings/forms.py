from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Room,Booking

# Форма для регистрации пользователя
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('number','description','price','photo',)
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('room','check_in','check_out')