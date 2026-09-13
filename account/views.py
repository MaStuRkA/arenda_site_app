from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.contrib import messages
from .forms import UserFormLogin, UserFormRegister, ResetPasswordForm, EmailResetForm, ChangePasswordForm
from account.models import CustomUser
from.utils import get_client_ip
from .logic_account import correct_user_send_email, correct_auth_user, session_in_correct, cheak_session_code, cheak_code_time_try, save_password_user_form
# Create your views here.
class LoginUser(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return redirect('arenda_app:home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = UserFormLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            correct_user = correct_auth_user(request, email, password)
            if correct_user is True:
                return redirect('arenda_app:home')
            else:
                messages.error(request, 'Такого пользователя не существует')
        return redirect("account:login")

    def get(self, request, *args, **kwargs):
        form = UserFormLogin()
        return render(request, "account/login.html", {"form":form})

class RegisterView(CreateView):
    model = CustomUser
    form_class = UserFormRegister
    template_name = 'account/register.html'
    success_url = reverse_lazy('account:login')
    context_object_name = 'form'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return redirect('arenda_app:home')
        return super().dispatch(request, *args, **kwargs)   

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

class EmailResetPassword(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return redirect('arenda_app:home')
        return super().dispatch(request, *args, **kwargs)
       
    def get(self, request, *args, **kwargs):
        form = EmailResetForm()
        return render(request, 'account/email_form_reset.html', {'form':form})

    def post(self, request, *args, **kwargs):
        form = EmailResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            correct = correct_user_send_email(request, email)
            if correct is True:
                return redirect('account:reset_code', email=email)
        return render(request, 'account/email_form_reset.html', {'form':form})

class ResetPassword(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return redirect('arenda_app:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        form = ResetPasswordForm()
        return render(request, 'account/reset_password.html', {'form':form})

    def post(self, request,email, *args, **kwargs):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            user_ip = get_client_ip(request)
            code = form.cleaned_data['code']
            session_in_correct(request, user_ip)
            if request.session.get(f'code_reset_{email}') is None:
                return redirect('account:login')
            # проверяет сессию на корректность. Если код не совпадает, возвращает число и дальше его передаю в функциюкак аргумент
            correct_code = cheak_session_code(request, code, user_ip, email)
            if correct_code is True:
                return redirect('account:change_password', email=email)
            # функция возвращает None, просто учитывает сессии.
            code_try_time = cheak_code_time_try(request, email, user_ip, correct_code)
        return render(request, 'account/reset_password.html', {'form':form})

class ChangePassword(View):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return redirect('arenda_app:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, email, *args, **kwargs):
        if request.session.get(f'change_password_{email}') is None:
            messages.error(request, 'Время изменения пароля истекло.')
            return redirect('account:login')
        form = ChangePasswordForm()
        return render(request, 'account/change_password.html', {'form':form})

    def post(self, request, email, *args, **kwargs):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if request.session.get(f'change_password_{email}') is None:
                messages.error(request, 'Время изменения пароля истекло.')
                return redirect('account:login')
            password1 = form.cleaned_data['password1']
            save_password = save_password_user_form(request, email, password1) # сохранение пароля пользователя, хешируя его.
            if save_password is True:
                return redirect('account:login')
        return render(request, 'account/change_password.html', {'form':form})

