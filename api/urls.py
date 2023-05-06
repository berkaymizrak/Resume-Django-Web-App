from rest_framework import routers
from api.views import ExternalProgramView
from django.urls import path, include

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('external_program/', ExternalProgramView.as_view(), name='external_program'),
]
