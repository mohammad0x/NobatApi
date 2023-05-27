from .views import *
from django.urls import path
from knox import views as knox_views

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/registerHair/', RegisterHairAPI.as_view(), name='register_hair'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/categoryCreateService/', categoryCreateService.as_view(), name='CategoryCreateService'),
    path('api/createService/<int:id>', createService.as_view(), name='createService'),
    path('api/categoryCreate/<int:id>', categoryCreate.as_view(), name='categoryCreate'),
    path('api/createService/<int:id>', createService.as_view(), name='createService'),
    path('api/profile', ProfileView.as_view(), name='profileView'),
]