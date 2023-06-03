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
    path('api/updateCreateService/<int:pk>', UpdateCreateService.as_view(), name='UpdateCreateService'),
    path('api/service', service.as_view(), name='service'),
    path('api/updateService/<int:pk>', UpdateService.as_view(), name='UpdateService'),
    path('api/deleteService/<int:pk>', deleteService.as_view(), name='deleteService'),
    path('api/reserve/<int:id>', reserve.as_view(), name='deleteService'),
    path('api/add_post/<int:id>', add_post.as_view(), name='addpost'),
    path('api/delete_post/<int:pk>', delete_post.as_view(), name='delete_post'),
    path('api/myService', myService.as_view(), name='myService'),
]