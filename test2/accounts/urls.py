# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import logout_view, register, edit_profile, profile, UserLoginView, home_view,  inventory_view, add_item_view, item_detail_view, delete_item_view
from . import views


urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('logout/', logout_view, name='logout'),
    path('list/', inventory_view, name='inventory'),
    path('add/', add_item_view, name='add_item'),
    path('item/<int:item_id>/', item_detail_view, name='item_detail'),
    path('item/<int:item_id>/delete/', delete_item_view, name='delete_item'),
]