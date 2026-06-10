from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list_view, name='order_list'),
    path('create/', views.order_create_view, name='order_create'),
    path('close/<int:order_id>/', views.order_close_view, name='order_close'),
]