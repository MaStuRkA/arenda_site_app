from rest_framework.views import APIView
from .serializers import BasketSerializersApi
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .basket_cart import Basket
from .logic_arenda_app import get_id_room
from urllib.parse import unquote
from .models import Hotel

class BasketAddViewAPI(APIView):
    def post(self, request,name, hotel, *args, **kwargs):
        serializers = BasketSerializersApi(data=request.data)
        if serializers.is_valid():
            total_price = serializers.validated_data['total_price']
            check_in = serializers.validated_data['check_in']
            check_out = serializers.validated_data['check_out']
            name_decoded = unquote(name)
            hotel_decoded = unquote(hotel)
            room_id = get_id_room(name_decoded, hotel_decoded)       
        # 3. Инициализируем корзину и добавляем данные
            check_in_str = check_in.strftime('%Y-%m-%d') if hasattr(check_in, 'strftime') else check_in
            check_out_str = check_out.strftime('%Y-%m-%d') if hasattr(check_out, 'strftime') else check_out
            basket = Basket(request)
        # Передаем не только id, но и пришедшие даты/цену
            basket.add(room_id=room_id, check_in=check_in_str, check_out=check_out_str, total_price=total_price)
        # 4. Возвращаем JSON с флагом 'success', который ждет ваш JS-код
            return Response({'status': 'success'})
        return Response(serializers.error, status=status.HTTP_400_BAD_REQUEST)

class LikedHotelsAPI(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, hotel_id, *args, **kwargs):
        hotel = Hotel.objects.filter(id=hotel_id).first()
        user = request.user
        if not hotel:
            return Response({'error':'Invalid hotels'}, status=400)
        if hotel.like.filter(id=user.id).exists():
            hotel.like.remove(user)
            liked = False
        else:
            hotel.like.add(user)
            liked = True
        return Response({'liked':liked})

class LikedListAPI(APIView):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            list_like_hotels = Hotel.objects.filter(like=user).values_list('id')
        else:
            list_like_hotels = []
        return Response({'list_like_hotels':list_like_hotels})