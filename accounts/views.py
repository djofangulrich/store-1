from django.contrib import messages
from django.conf import settings as django_settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, CreateView

from accounts.forms import LoginForm
from accounts.models import CustomUser


class Login(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        messages.success(self.request, f'Connexion réussie !')
        context.update(
            {
                self.redirect_field_name: self.get_redirect_url(),
                "site": current_site,
                "site_name": current_site.name,
                **(self.extra_context or {}),
                "messages": messages,
            }
        )
        return context


class Register(View):

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, 'accounts/register.html', locals())

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Bienvenue {username}; Votre compte a été créer avec succès')
            return redirect('home')


class Profil(DetailView):
    model = CustomUser
    template_name_field = "accounts/profil.html"


class ChangePassword(PasswordChangeView):
    template_name = "accounts/change-password.html"
    title = _("Modifier le mot de passe")
    success_url = reverse_lazy("accounts:profil")


@login_required()
def profil(request):
    return render(request, 'accounts/profil.html', locals())


User = get_user_model()


class Signup(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "accounts/register.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_anonymous and not request.user.is_superuser:
            return redirect("dashboard:home")
        if not django_settings.ACCOUNT_HANDLING:
            return redirect(django_settings.SIGNUP_URL)
        if not request.user.is_superuser and not django_settings.ACCOUNT_SIGNUP_ALLOWED:
            c = {"error_msg": _("Account signup is only allowed for administrators.")}
            return render(request, "error.html", context=c)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["honeypot_class"] = context["form"].honeypot_class
        context["honeypot_jsfunction"] = context["form"].honeypot_jsfunction
        return context

    def get_success_url(self, *args):
        messages.success(
            self.request, _("You are now signed up... and now you can sign in!")
        )
        return reverse("accounts:login")
