from django.urls import path

from listings import views

urlpatterns = [
    path('units/', views.ListingView.as_view(), name='units')
]
