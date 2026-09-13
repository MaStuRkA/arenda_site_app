from django import forms
from django.contrib.auth.models import User

# Предположим, что Город и Отчество хранятся в связанной модели Profile
class UserDetailsForm(forms.ModelForm):
    otchestvo = forms.CharField(label="Отчество", required=False)
    city = forms.ChoiceField(label="Город", choices=[('msk', 'Москва'), ('spb', 'Санкт-Петербург')])

    class Meta:
        model = User
        fields = ['last_name', 'first_name']
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
        }

class EmailVerificationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        labels = {
            'email': 'Электронная почта',
        }
