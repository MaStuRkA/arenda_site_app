from django.contrib import admin
from .models import Hotel, Room, RoomType, Review, Booking, Payment
# Register your models here.
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(Review)
admin.site.register(Booking)
admin.site.register(Payment)