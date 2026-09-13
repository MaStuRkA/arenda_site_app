from django.core.mail import send_mail
from account.logic_account import get_code
from .models import Hotel, RoomType

def get_id_room(name, hotel):
    hotel = Hotel.objects.filter(name=hotel).first()
    name_room = RoomType.objects.filter(name=name, hotel=hotel).first()
    return name_room.pk

def update_personal_date(request, surname, firstname, patronymic, city, phone):
    user = request.user
    date_all = {'surname':surname, 'first_name':firstname, 'last_name':patronymic, 'recomend_city':city, 'phone':phone}
    for key, value in date_all.items():
        if value != '':
            setattr(user, key, value)
    user.correct_profile = True
    user.save()

def send_email_and_correct_email(request, user, email):
    if not user.email == email:
        return f'Почты не совпадают. Укажите почту корректную почту.'
    request.session['attempt_email_code'] = 5
    code = get_code()
    request.session['code_email'] = code
    request.session['correct_attempt'] = True
    request.session.set_expiry(300)
    print(code)
    send_mail(
            subject='Подверждение почты',
            message=f'Код для подверждения: {code}',
            from_email='groww1twich@gmail.com',
            recipient_list=[email]
               )
    return True

def confirm_email_and_cheak_code(request, user, code, code_user, attempts):
    if attempts <= 0:
        return False
    if code_user != code:
        attempts -= 1
        request.session['attempt_email_code'] = attempts

    if code == code_user:
        user.confirm_email = True
        user.correct_profile = True
        user.save()
        return True

def del_session_confirm_email(request):
    del request.session['code_email']
    del request.session['correct_attempt']
    del request.session['attempt_email_code']



def liked_list_hotels(request, ):
    user = request.user
    if user.is_authenticated:
        list_like_hotels = Hotel.objects.filter(like=user).values_list('id', flat=True)
    else:
        list_like_hotels = []
    return list_like_hotels