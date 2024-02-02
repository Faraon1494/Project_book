from django.urls import path
from . import views



app_name = 'user_auth'

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cab/', views.change_user_data, name='cab'),
]