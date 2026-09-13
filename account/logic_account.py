from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from account.models import CustomUser
import secrets

def correct_auth_user(request, email, password):
    user = authenticate(request, username=email, password=password)
    if user is None:
        return False
    login(request, user)
    return True

def get_code():
    code_str = ''.join(str(secrets.randbelow(10)) for _ in range(6))
    print(code_str)
    return code_str

def correct_user_send_email(request,email):
    user = get_object_or_404(CustomUser, email=email)
    if user:
        code_str = get_code()
        send_mail(
                subject='Смена пароля',
                message=f'Код для подверждения: {code_str}',
                from_email='groww1twich@gmail.com',
                recipient_list=[email]
            )
        request.session[f'code_reset_{email}'] = code_str
        request.session.set_expiry(300)
        return True
    return False

def session_in_correct(request, user_ip):
    if request.session.get(f'try_{user_ip}') is None:
        request.session[f'try_{user_ip}'] = 4
        request.session.set_expiry(300)

def cheak_session_code(request, code, user_ip, email):
    if code == request.session.get(f'code_reset_{email}'):
        del request.session[f'code_reset_{email}']
        del request.session[f'try_{user_ip}']
        request.session[f'change_password_{email}'] = email
        request.session.set_expiry(300)
        return True
    request.session[f'try_{user_ip}'] -= 1
    code_time_try = request.session[f'try_{user_ip}']
    return code_time_try

def cheak_code_time_try(request, email, user_ip, code_time_try):
    if code_time_try is not True:
        if code_time_try <= 0:
            del request.session[f'code_reset_{email}']
            del request.session[f'try_{user_ip}']

def save_password_user_form(request, email, password1):
    request.session.pop(f'change_password_{email}')
    user = CustomUser.objects.get(email=email)
    user.set_password(password1)
    user.save()
    return True