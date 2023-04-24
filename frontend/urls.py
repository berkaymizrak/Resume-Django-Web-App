from django.urls import path
from frontend import views

urlpatterns = [
    path('', views.index, name='index'),
    path('20_mayis_nikah/', views.nikah, name='nikah'),
    path('21_mayis_dugun/', views.dugun, name='dugun'),
]
