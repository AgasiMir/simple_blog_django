from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "inputUsername",
                "type": "username",
                "placeholder": "Имя пользователя",
            }
        ),
    )

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "inputPassword",
                "type": "password",
                "placeholder": "Пароль",
            }
        ),
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "ReInputPassword",
                "type": "password",
                "placeholder": "Повторите пароль",
            }
        ),
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "password1", "password2"]
