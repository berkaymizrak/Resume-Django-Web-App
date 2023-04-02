from django.urls import path
from user import views

urlpatterns = [
    path('', views.index, name='index'),
    path('statistics', views.statistics, name='statistics'),
    path('<slug>/', views.special_links, name='special_links'),
]
