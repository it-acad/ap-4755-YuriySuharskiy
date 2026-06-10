from django.urls import include, path
from book import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('search/', views.book_search, name='book_search'),
]
