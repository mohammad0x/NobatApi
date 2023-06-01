from .views import *
from django.urls import path
from knox import views as knox_views

app_name = 'app'
urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/registerHair/', RegisterHairAPI.as_view(), name='register_hair'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/categoryCreateService/', categoryCreateService.as_view(), name='CategoryCreateService'),
    path('api/categoryCreate/<int:id>', categoryCreate.as_view(), name='categoryCreate'),
    path('api/profile', ProfileView.as_view(), name='profileView'),
    path('api/updateProfile/<int:pk>', UpdateProfile.as_view(), name='updateProfile'),
    path('api/createService/<int:id>', createService.as_view(), name='createService'),
    path('api/updateCreateService/<int:pk>', UpdateCreateService.as_view(), name='UpdateCreateService'),
    path('api/service', service.as_view(), name='service'),
    path('api/updateService/<int:pk>', UpdateService.as_view(), name='UpdateService'),
    path('api/deleteService/<int:pk>', deleteService.as_view(), name='deleteService'),
    path('api/reserve/<int:id>', reserve.as_view(), name='deleteService'),
    path('api/addImage/<int:id>', image.as_view(), name='addImage'),
    path('api/deleteImage/<int:pk>', deleteImage.as_view(), name='deleteImage'),
]