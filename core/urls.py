from django.urls import path
from core import views

urlpatterns = [
    path('statistics/', views.statistics, name='statistics'),
    path('<slug>/', views.special_links, name='special_links'),
]
