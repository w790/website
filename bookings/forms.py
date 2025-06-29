from .models import Room,Booking
from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser

class CustomSignupForm(SignupForm):
    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован")
        return email


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('number','description','price','photo',)

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('room','check_in','check_out')
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        # 1. Проверяем, что обе даты присутствуют
        if check_in is None or check_out is None:
            # Если какая-то дата отсутствует, пропускаем дальнейшие проверки
            return cleaned_data

        if check_in >= check_out:
            raise forms.ValidationError("Дата выезда должна быть позже даты заезда.")

        if room:
            # Получаем пользователя, если он есть
            user = getattr(self.instance, 'user', None)
            # Проверим, доступен ли номер
            booking = Booking(user=user, room=room, check_in=check_in, check_out=check_out)
            if not booking.is_available():
                raise forms.ValidationError("Этот номер уже забронирован на выбранные даты.")

        return cleaned_data
