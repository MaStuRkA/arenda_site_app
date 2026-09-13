from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from account.models import CustomUser
from django.urls import reverse
# Create your models here.


"""Модель отеля"""

# придумать логику лайка

class Hotel(models.Model):
    img = models.ImageField(blank=True, null=True, default='meida_img/logo_arenda.png', upload_to='hotel_img/')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],  null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(CustomUser, related_name='like_hotels', blank=True)

    def __str__(self):
        return f'{self.name}'

"""Модель тип комнаты"""
class RoomType(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types')
    name = models.CharField(max_length=100) # Например: "Двухместный Люкс"
    capacity = models.IntegerField(help_text="Максимальное количество гостей")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Цена за одну ночь")
    description = models.TextField(blank=True)

    def __str__(self):
        return f' Отель {self.hotel}, номер {self.name}'

    def get_absolute_url(self):
        return reverse('arenda_app:booking',args=[self.name, self.hotel])
    

class Room(models.Model):
    """Конкретная физическая комната"""
    STATUS_CHOICES = [
        ('available', 'Доступен'),
        ('maintenance', 'Ремонт/Обслуживание'),
    ]
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='rooms')
    number = models.CharField(max_length=10, help_text="Номер комнаты (например, 301)")
    floor = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    class Meta:
        # Уникальный номер комнаты в пределах одного отеля
        unique_together = ('room_type', 'number')

    def __str__(self):
        return f"Комната {self.number} ({self.room_type.name})"

class Booking(models.Model):
    """Связующая модель для бронирования"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('confirmed', 'Подтверждено'),
        ('cancelled', 'Отменено'),
        ('checked_in', 'Заселен'),
        ('checked_out', 'Выехал'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Бронь #{self.id} - {self.user.username} (Комната {self.room.number})"

class Payment(models.Model):
    """Логирование транзакций"""
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('completed', 'Оплачено'),
        ('failed', 'Ошибка'),
        ('refunded', 'Возврат'),
    ]
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID транзакции платежной системы")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid_at = models.DateTimeField(blank=True, null=True)

class Review(models.Model):
    """Отзывы пользователей"""
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)