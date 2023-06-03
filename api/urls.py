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
    path('api/addPost/<int:id>', addPost.as_view(), name='addImage'),
    path('api/deletePost/<int:pk>', deletePost.as_view(), name='deleteImage'),
    path('api/search/<str:searchs>', Search.as_view(), name='Search'),
    path('api/myService', myService.as_view(), name='myService'),
    path('api/Hair_stylist/<int:id>', Hair_stylist.as_view(), name='Hair_stylist'),
]