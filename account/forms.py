

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import CustomUser
import string
from django.core.exceptions import ValidationError
'''
def clean_username(self):
    username = self.cleaned_data['username']
    if "@!&?$" in username:
        raise forms.ValidationError("Замените знаки не соотвествующие для имени: @!?&$")
'''

error_email = ['@evonext.com', '@hq0.net', '@maildrop.cc', '@mohmal.im']

def validate_password_custom(password):
        symbol = string.punctuation # Это пунктуации. строка всех пунктуаций
        dig_cnt = sum(1 for pas in password if pas.isdigit()) # считаю цифры в пароле
        sym_cnt = sum(1 for pas in password if pas in symbol) # считаю пунктуации в пароле
        len_password = len(password)
        if len_password < 16:
            raise forms.ValidationError('Пароль короткий. Минимум 16 символов.')
        if dig_cnt + sym_cnt < 6:
            raise forms.ValidationError(f'Пароль должен содержать символы пунктуации. {symbol}')
        
def validate_code(code):
    if not code.isdigit():
        raise ValidationError('Должен содержать цифры.')

class UserFormLogin(forms.Form):
    email = forms.EmailField(label='email')
    password = forms.CharField(widget=forms.PasswordInput(), label='password')

class UserFormRegister(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(),validators=[validate_password_custom])
    username = forms.CharField(max_length=150, help_text='', label='Имя пользователя')
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']


    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) <= 3:
            raise forms.ValidationError('Имя пользователя слишком короткое')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        res = any(em for em in error_email if em in email)
        if res is True:
            raise forms.ValidationError('Регистрация с временной почты. такая почта не подходит.')
        return email

class ResetPasswordForm(forms.Form):
    code = forms.CharField(max_length=6, validators=[validate_code])

    def clean_code(self):
        code = self.cleaned_data['code']
        if code.isdigit():
            if len(code) == 6:
                return code
            else:
                raise forms.ValidationError('Введите все цифры из сообщения')
        else:
            raise forms.ValidationError('Код должен содержать цифры.')

class EmailResetForm(forms.Form):
    email = forms.EmailField()


    def clean_email(self):
        email = self.cleaned_data['email']
        res = any(em for em in error_email if em in email)
        if res is True:
            raise forms.ValidationError('Временные почты не могут зарегестрироваться.')
        return email

class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(),validators=[validate_password_custom])
    password2 = forms.CharField(widget=forms.PasswordInput())


    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        
        return cleaned_data


