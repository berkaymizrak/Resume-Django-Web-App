from django.urls import path
from frontend import views

urlpatterns = [
    path('', views.index, name='index'),
    path('statistics/', views.statistics, name='statistics'),
    # path('21_mayis_nikah/', views.invitation, name='invitation'),
]
