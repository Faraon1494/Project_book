from django.urls import path
from . import views
from .views import *

app_name = 'main' 

urlpatterns = [
    path('', views.index, name='index'),
    path('cheap/', views.cheap, name='cheap'),
    path('item/<int:item_id>/', views.detail, name = 'detail'),
    path('add/', views.add_product, name='add'),
    path('create/', views.create_book, name='create_book'),
    path('item/<int:item_id>/update/', views.update_book, name='update_book'),
    path('item/<int:item_id>/delete/', views.delete_book, name='delete_book'),
]
