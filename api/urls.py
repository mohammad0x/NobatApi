from .views import *
from django.urls import path
from django.contrib.auth import views as auth_views
from knox import views as knox_views

app_name = 'app'
urlpatterns = [
    path('api/', Home.as_view(), name='home'),
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
    path('api/like/<int:id>', like.as_view(), name='like'),
    path('api/dislike/<int:id>', dislike.as_view(), name='like'),
    # reset password
    path('api/password-reset/', auth_views.PasswordResetView.as_view(template_name='api/password_reset.html',
                                                                 success_url=reverse_lazy('password_reset_done')),
         name='password_reset'),
    path('api/password-reset-confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('api/password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='api/password_reset_done.html'),
         name='password_reset_done'),


    path('api/password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='api/password_reset_complete.html'),
         name='password_reset_complete'),

]
