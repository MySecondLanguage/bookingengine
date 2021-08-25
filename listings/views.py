from rest_framework import generics



from listings.models import HotelRoom, HotelRoomType, Listing

from listings.serializers import ListingSerializer

from django.db.models import Exists, F, OuterRef, Q, Value
from django.forms.fields import BooleanField
from rest_framework.response import Response


class ListingView(generics.ListAPIView):
    serializer_class = ListingSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                'items': serializer.data
            }
        )

    def get_queryset(self):
        params = self.request.query_params
    
        check_in = params.get('check_in', '')
        check_out = params.get('check_out', '')
        max_price = params.get('max_price', 100)

        if check_in and check_out:
            # available hotel
            hotel = Listing.objects.annotate(
                is_room_available=Exists(
                    HotelRoomType.objects.exclude(
                        room_day_slots__spot__range=[check_in, check_out],                     
                    ).filter(
                        hotel=OuterRef('pk')
                    )
                ),
                price=F('booking_info__price')
            ).filter(
                listing_type='hotel',
                booking_info__price__lte=max_price
            ).exclude(
                is_room_available=False
                
            )
            
            # available apartment
            apartment = Listing.objects.annotate(
                is_room_available=Value(True), # to avoid error during union
                price=F('booking_info__price')
            ).filter(
                listing_type='apartment',
                booking_info__price__lt=max_price
            ).exclude(
                apartment_day_slots__spot__range=[check_in, check_out]
            )
            
            # union
            queryset = apartment.union(hotel)
        
        else: # if no paramter
            queryset = Listing.objects.annotate(price=F('booking_info__price'))
    
        return queryset.order_by('price')
