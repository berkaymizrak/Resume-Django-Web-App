from django.urls import path
from frontend import views

urlpatterns = [
    path('', views.index, name='index'),
    path('21_mayis_nikah/', views.invitation, name='invitation'),
]
