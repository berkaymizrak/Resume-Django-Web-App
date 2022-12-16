from django.urls import path
from user import views

urlpatterns = [
    path('', views.index, name='index'),

    path('<slug>/', views.special_links, name='special_links'),
]
