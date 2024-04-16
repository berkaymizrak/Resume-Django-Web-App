from core import views
from django.urls import path

urlpatterns = [
    path('blocked/', views.csrf_failure, name='csrf_failure'),
]
