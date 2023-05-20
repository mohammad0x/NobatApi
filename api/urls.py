from .views import *
from django.urls import path

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),

]