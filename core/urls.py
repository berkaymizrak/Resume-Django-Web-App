from core import views
from django.urls import path

urlpatterns = [
    path('blocked/', views.blocked_user, name='blocked_user'),
]
