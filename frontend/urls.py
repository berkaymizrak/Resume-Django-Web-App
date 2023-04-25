from django.urls import path
from frontend import views

urlpatterns = [
    path('', views.index, name='index'),
    path('21_mayis_dugun/', views.invitation, name='invitation'),
]
