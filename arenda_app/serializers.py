from rest_framework import serializers


class BasketSerializersApi(serializers.Serializer):
    total_price = serializers.IntegerField()
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    
    
    