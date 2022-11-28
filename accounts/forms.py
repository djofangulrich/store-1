from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField


class LoginForm(AuthenticationForm):
    username = UsernameField(max_length=255,
                             widget=forms.TextInput(
                                 attrs={'name': 'user', 'id': 'user', 'placeholder': 'Nom d\'utilisateur',
                                        'class': 'form__input', "autofocus": True}))
    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(
                                   attrs={'name': 'password', 'id': 'password', 'placeholder': 'Mot de passe',
                                          'class': 'form__input'}))

    error_messages = {
        "invalid_login": _(
            "Veillez entrer un %(username)s et Mot de passe valident. Note that both ",
            "Ces champs sont sensible à la casse"
        ),
        "inactive": _("Ce compte est inactif."),
    }


class RegisterForm(UserCreationForm):
    username = UsernameField(max_length=255,
                             widget=forms.TextInput(
                                 attrs={'name': 'user', 'id': 'user', 'placeholder': 'Nom d\'utilisateur',
                                        'class': 'form__input', "autofocus": True}))
    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(
                                   attrs={'name': 'password', 'id': 'password', 'placeholder': 'Mot de passe',
                                          'class': 'form__input'}))
