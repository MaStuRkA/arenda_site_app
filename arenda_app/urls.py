from django.urls import path
from .views import IndexView, ProfileView, SettingsView, ConfirmEmailSettingsView, logoit_system, BookingHotelView, BasketView, LiekdHotelView
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .api_view import BasketAddViewAPI, LikedHotelsAPI

app_name = 'arenda_app'

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('like/<int:hotel_id>/api/', LikedHotelsAPI.as_view(), name='like_hotel'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/likehotel', LiekdHotelView.as_view(), name='hotels_like'),
    path('profile/settings/', SettingsView.as_view(), name='settings'),
    path('verify-email/', ConfirmEmailSettingsView.as_view(), name='confirm_code_email'),
    path('<str:name>/<str:hotel>/', BookingHotelView.as_view(), name='booking'),
    path('<str:name>/<str:hotel>/api/basket/', BasketAddViewAPI.as_view(), name='add-basket'),
    path('logout/', views.logoit_system, name='logout'),
    path('basket/', BasketView.as_view(), name='basket'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)