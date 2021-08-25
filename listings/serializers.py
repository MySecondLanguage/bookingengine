from rest_framework import serializers
from listings.models import Listing


class ListingSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    class Meta:
        model = Listing
        fields = '__all__'

    def get_price(self, obj):
        if hasattr(obj, 'booking_info'):
            return obj.booking_info.price
        return None

