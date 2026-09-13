from arenda_app.models import RoomType

class Basket():
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('room_type')
        if basket is None:
            self.session['room_type'] = {}
        self.basket = basket

    def add(self, room_id, check_in, check_out, total_price):
        room_id = str(room_id)
        if room_id not in self.basket:
            self.basket[room_id] = {'room_id':room_id, 'check_in':check_in, 'check_out':check_out, 'total_price':total_price}
        else:
            self.basket[room_id]['check_in'] = check_in
            self.basket[room_id]['check_out'] = check_out
            self.basket[room_id]['total_price'] = total_price
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        if self.basket is not None:
            room_ids = self.basket.keys()
            rooms = RoomType.objects.filter(id__in=room_ids)
            basket_copy = self.basket.copy()

            for room in rooms:
                room_id = str(room.id)
                if room_id in basket_copy:
                    basket_copy[room_id]['room_object'] = room

            for item in basket_copy.values():
                yield item
        

        
        