from django.shortcuts import render, redirect
from urllib.parse import unquote
from django.views.generic import ListView, DetailView, View, TemplateView
from .models import Hotel, RoomType, Room
from account.models import CustomUser
from .logic_arenda_app import update_personal_date, send_email_and_correct_email, confirm_email_and_cheak_code, del_session_confirm_email, get_id_room, liked_list_hotels
from django.contrib import messages
from django.contrib.auth import logout
from .basket_cart import Basket
import json
from django.http import JsonResponse
# Create your views here.

def logoit_system(request):
    logout(request)
    return redirect('account:login')

class IndexView(ListView):
    model = Hotel
    template_name = 'arenda_app/index.html'
    context_object_name = 'hotels'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(liked_list_hotels(self.request))
        context['data_liked'] = liked_list_hotels(self.request)
        return context

    

class ProfileView(DetailView):
    model = CustomUser
    template_name = 'arenda_app/profile.html'
    context_object_name = 'profile'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            return redirect('account:login')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset = None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['title'] = user.username
        context['class'] = 'profile'
        return context

class SettingsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'arenda_app/settings_profile.html', {'class':'settings'}) # указывать class чтобы обводка была в боковой менюшке

    def post(self, request, *args, **kwargs):
        if 'submit_personal_data' in request.POST:
            surname = request.POST.get('surname')
            firstname = request.POST.get('firstname')
            last_name = request.POST.get('last_name')
            city = request.POST.get('city')
            phone = request.POST.get('phone')
            update_personal_date(request,surname, firstname, last_name, city, phone)
            return redirect('arenda_app:profile')
        if 'submit_email_verification' in request.POST:
            user = request.user
            email = request.POST.get('email')
            if email:
                correct_and_error = send_email_and_correct_email(request, user, email)
            else:
                messages.error(request, 'Введите почту.')
                return redirect('arenda_app:settings')
            if correct_and_error is True:
                return redirect('arenda_app:confirm_code_email')
            messages.error(request, f'{correct_and_error}')
            return redirect('arenda_app:settings')

class ConfirmEmailSettingsView(View):
    def get(self, request, *args, **kwargs):
            if request.session.get('correct_attempt') is True:
                return render(request, 'arenda_app/confirm_email.html')
            messages.error(request, 'Попытки истекли.')
            return redirect('arenda_app:profile')

    def post(self, request, *args, **kwargs):
        user = request.user
        attempts = request.session.get('attempt_email_code')
        code_user = request.POST.get('code')
        code = request.session.get('code_email')
        validate_email = confirm_email_and_cheak_code(request, user, code, code_user, attempts)
        if validate_email is True:
            del_session_confirm_email()
            return redirect('arenda_app:profile')
        
        if validate_email is False:
            del_session_confirm_email()
            messages.error(request, 'попытки исчерпаны! Попробуйте еще раз!')
            return redirect('arenda_app:settings')
        return render(request, 'arenda_app/confirm_email.html')

class BookingHotelView(DetailView):
    model = Hotel
    template_name = 'arenda_app/booking_form.html'
    context_object_name = 'room_type'

    def get_object(self, queryset=None):
        slug_room = unquote(self.kwargs['name'])
        slug_hotel = unquote(self.kwargs['hotel'])
        hotel = Hotel.objects.get(name=slug_hotel)
        room_type = RoomType.objects.get(hotel=hotel, name=slug_room)
        return room_type

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug_room = unquote(self.kwargs['name'])
        slug_hotel = unquote(self.kwargs['hotel'])
        room_type = get_id_room(slug_room, slug_hotel) # ПЕРЕДЕЛАЛ ВЫГРУЗКУ ИЗОБРАЖЕНИЯ
        context['hotel'] = Hotel.objects.filter(name=slug_hotel).first()
        context['room'] = Room.objects.filter(room_type=room_type).first()
        return context
        
class BasketView(TemplateView):
    template_name = 'arenda_app/basket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket'] = Basket(self.request) if Basket(self.request) is not None else None
        return context
    

class SearchView(View):
    pass

class LiekdHotelView(ListView):
    model = Hotel
    template_name = 'arenda_app/liked_hotel.html'
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['liked_hotels'] = Hotel.objects.filter(like=user)
        return context



