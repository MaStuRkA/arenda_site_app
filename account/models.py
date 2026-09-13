from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('guest', 'Гость'),
        ('manager', 'Менеджер отеля'),
        ('admin', 'Администратор'),
    ]
    CITY_CHOICES = [
    ('moscow', 'Москва'),
    ('saint_petersburg', 'Санкт-Петербург'),
    ('novosibirsk', 'Новосибирск'),
    ('ekaterinburg', 'Екатеринбург'),
    ('kazan', 'Казань'),
    ('nizhny_novgorod', 'Нижний Новгород'),
    ('chelyabinsk', 'Челябинск'),
    ('samara', 'Самара'),
    ('omsk', 'Омск'),
    ('rostov_on_don', 'Ростов-на-Дону'),
]
    confirm_email = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='guest')
    phone = models.CharField(max_length=20, blank=True)
    recomend_city = models.CharField(default='Укажите город', choices=CITY_CHOICES)
    correct_profile = models.BooleanField(default=False)
    username = models.CharField(db_index=True, max_length=150, unique=False, blank=True, null=True)
    surname = models.CharField(max_length=150, unique=False, blank=True, null=True)
    
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    # ... остальные ваши поля ...

    USERNAME_FIELD = 'email'

    # 2. Убираем 'username' отсюда, иначе Django потребует его при `createsuperuser`
    REQUIRED_FIELDS = []


    def __str__(self):
        return f'{self.email}'


