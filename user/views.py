import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import RedirectView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import BaseSignupForm, BaseProfileForm
from .models import RegistrationToken


class UserLoginView(LoginView):
    template_name = 'user/login.html'


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You are successfully logged out.")

        return super().dispatch(request, *args, **kwargs)


class UserRegistrationView(CreateView):
    model = User
    form_class = BaseSignupForm
    template_name = 'user/signup.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        messages.success(
            self.request,
            "Your account was successfully created, but needs verification. We send you an email with activation link. "
            "Please activate your account within next 20 minutes."
        )

        return super().form_valid(form)


class UserConfirmationView(RedirectView):
    def dispatch(self, request, token, *args, **kwargs):
        from django.utils import timezone

        registration_token = RegistrationToken.objects.get(token=token)
        if registration_token:
            user = registration_token.user
            if registration_token.valid_to <= timezone.now():
                user.active = True
                user.save()

                messages.success(request, "Congratulations, your user account now is activated.")
            else:
                logging.log(logging.INFO, f'Registration token "{token}" is expired and will be removed.')
                registration_token.delete()
        else:
            logging.log(logging.ERROR, f'Registration token "{token}" not found.')

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self):
        return reverse_lazy('homepage')


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = BaseProfileForm
    template_name = 'user/profile.html'

    def form_valid(self, form):
        messages.success(self.request, "Your profile was successfully updated.")

        return super().form_valid(form)

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile')


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'user/change_password.html'

    def form_valid(self, form):
        messages.success(self.request, "Password was successfully changed.")

        return super().form_valid(form)

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile')
