from django.urls import path
from link_management import views

urlpatterns = [
    path('<slug>/', views.special_links, name='special_links'),
]
