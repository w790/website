from django import forms
from bookings.models import CustomUser
from django.contrib.auth.forms import UserCreationForm

#UserCreationForm - Это встроенная в Django форма для создания новых пользователей.
#Она содержит три поля: `username`, `password1`, `password2` (подтверждение пароля).
#Автоматически проверяет:Уникальность имени пользователя, Соответствие двух паролей, Сложность пароля


# Форма для регистрации пользователя
class CustomUserCreationForm(UserCreationForm):
    #Мы расширяем стандартную форму, добавляя поле `email` (обязательное)
    email = forms.EmailField(required=True)
    #Meta в Django - это просто контейнер для настроек
    #Когда Django видит класс Meta, он автоматически:Берет указанную модель (User),
    # Для каждого поля в fields:Смотрит, есть ли такое поле в модели, Создает соответствующее поле формы, Применяет стандартные настройки (валидаторы и т.д.)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email