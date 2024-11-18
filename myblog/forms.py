from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from myblog.models import Contact, Comment


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


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "name", "placeholder": "Ваше имя"}
        ),
    )

    email = forms.CharField(
        max_length=100,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "id": "email", "placeholder": "Ваша почта"}
        ),
    )

    # subject = forms.CharField(
    #     max_length=200,
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "id": "subject", "placeholder": "Тема"}
    #     ),
    # )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control md-textarea",
                "id": "message",
                "rows": 2,
                "placeholder": "Ваше сообщение",
            }
        )
    )

    class Meta:
        model = Contact
        fields = ["subject", "name", "email", "body"]

        widgets = {"body": forms.Textarea(attrs={"cols": 60, "rows": 10})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control mb-3", "rows": 3}),
        }
