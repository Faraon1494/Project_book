from django.urls import path
from . import views 

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('buy_fondy/', views.buy_fondy, name='buy_fondy'),
    path('show_client_location/', views.show_client_location, name='show_client_location'),
    path('save_location/', views.save_location, name='save_location'),
    path('geolocations/', views.geolocations, name='geolocations'),
    # path('create_payment_intent/', views.create_payment_intent, name='create_payment_intent'),
]