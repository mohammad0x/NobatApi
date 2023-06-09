import json

from allauth.account.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework import viewsets
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import *
from .models import MyUser
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, Http404


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class RegisterHairAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializerHair

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class categoryCreateService(APIView):
    def get(self, request, format=None):
        data = Category_createService.objects.all().values()
        return Response(data)

    def post(self, request, *args, **kwargs):
        data = {
            'title': request.data.get('title'),
            'image': request.data.get('image'),
            'status': request.data.get('status')
        }
        serializer = Category_createServiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UpdateCreateService(RetrieveUpdateAPIView):
    serializer_class = CreateServiceSerializer
    queryset = Create_Service.objects.all()

class categoryCreate(APIView):
    def get(self, request, id):
        data = get_object_or_404(Category_Service, id=id, status=True)

        return JsonResponse({
            'id': data.id,
            'title': data.title,
            'image': data.image.url,
            'status': data.status,
            'position': data.position,
        }, status=status.HTTP_200_OK)

class categoryService(APIView):
    def get(self, request, id):
        data = Category_Service.objects.filter(services_id=id).values()
        return Response(data)

class ProfileView(APIView):
    def get(self, request):
        profile = Profile.objects.get(user_id=request.user.id)

        return JsonResponse({
            'id': profile.id,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'nationality_code': profile.nationality_code,
            'phone': profile.phone,
            'verify_code': profile.verify_code,
            'city': profile.city,
            'address': profile.address,
            'photo': profile.photo.url,
        }, status=status.HTTP_200_OK)


class UpdateProfile(RetrieveUpdateAPIView):
    serializer_class = ProfileUppdateSerializer
    queryset = Profile.objects.all()


class service(generics.GenericAPIView):
    serializer_class = ServiceSerializer

    def post(self, request, *args, **kwargs):
        data = {
            'user': request.user.id,
            'service': request.data.get('service'),
            'category': request.data.get('category'),
            'title': request.data.get('title'),
            'price': request.data.get('price'),
            'desc': request.data.get('desc'),
            'active': request.data.get('active'),
        }
        serializer = ServiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateService(RetrieveUpdateAPIView):
    serializer_class = ServiceUpdateSerializer
    queryset = Service.objects.all()

class deleteService(generics.GenericAPIView):
    model = Service
    serializer_class = ServiceSerializer

    def get_object(self, pk):
        try:
            return Service.objects.get(user=self.request.user, pk=pk)
        except Service.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        object = self.get_object(pk)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class reserve(generics.GenericAPIView):
    serializer_class = ReserveSerializer
    def post(self, request, id, *args, **kwargs):
        data = {
            'user': request.user.id,
            'service': id,
            'number': request.data.get('number'),
            'busy': request.data.get('busy'),
            'date': request.data.get('date'),
            'time': request.data.get('time'),
        }
        serializer = ReserveSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class addPost(generics.GenericAPIView):
    serializer_class = ImageSerializer
    def post(self, request, id, *args, **kwargs):
        data = {
            'poster': id,
            'image': request.data.get('image'),
        }
        serializer = ImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class deletePost(generics.GenericAPIView):
    model = Image
    serializer_class = ImageSerializer

    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        object = self.get_object(pk)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Search(APIView):
    def get(self, request, searchs):
        if searchs:
            if Service.objects.filter(Q(title=searchs)).exists():
                data = Service.objects.filter(Q(title=searchs)).values()
                return Response(data)
            elif Create_Service.objects.filter(Q(title=searchs) | Q(slug=searchs)).exists():
                data = Create_Service.objects.filter(Q(title=searchs) | Q(slug=searchs)).values()
                return Response(data)
            else:
                return Response(None)

class myService(APIView):
    def get(self, request):
        data = Service.objects.filter(user_id=request.user.id).values()
        return Response(data)

class Hair_stylist(generics.GenericAPIView):
    models = Comment
    serializer_class = CommentSerializer
    def post(self, request, id, *args, **kwargs):
        is_reply = request.data.get('is_reply')
        print(is_reply)
        if is_reply is None:
            data = {
                'user': request.user.id,
                'reply': None,
                'rate':request.data.get('rate'),
                'desc':request.data.get('desc'),
                'date': timezone.now(),
                'post_key':id,
                'is_reply': False
            }
        else:
            data = {
                'user': request.user.id,
                'reply': '2',
                'rate':request.data.get('rate'),
                'desc':request.data.get('desc'),
                'date': timezone.now(),
                'post_key':id,
                'is_reply': True
            }
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request,id):
        profile = get_object_or_404(Profile, user_id=id)
        service = Service.objects.filter(user_id=id).values()
        create_service = Create_Service.objects.get(user_id=id)
        image = Image.objects.filter(poster_id=create_service.id).values()

        return Response({
            'service': service,
            'profile':{
                'id': profile.id,
                'first_name': profile.first_name,
                'last_name': profile.last_name,
                'nationality_code': profile.nationality_code,
                'phone': profile.phone,
                'verify_code': profile.verify_code,
                'city': profile.city,
                'address': profile.address,
                'photo': profile.photo.url,
            },
            'create_service':{
                'title': create_service.title,
                'slug': create_service.slug,
                'image': create_service.image.url,
                'score': create_service.score,
                'publish': create_service.publish,
                'edit': create_service.edit,
            },
            'image':image,
        })

class Home(APIView):
    def get(self, request):
        return Response({
            'data_CategoryCreateService': Category_createService.objects.filter(status=True).values(),
            'data_Create_Service': Create_Service.objects.filter(edit=True).order_by('-publish').values()
        })

class like(APIView):
    model = Like
    serializer_class = LikeSerializer
    def post(self, request, id):
        data = {
            'user': request.user.id,
            'image': id
        }
        serializer = LikeSerializer(data=data)
        like = Like.objects.filter(image_id=id, user_id=request.user.id)
        print(like)
        if like.exists():
            like.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class dislike(APIView):
    model = DisLike
    serializer_class = DisLikeSerializer

    def post(self, request, id):
        data = {
            'user': request.user.id,
            'image': id
        }
        serializer = DisLikeSerializer(data=data)
        dislike = DisLike.objects.filter(image_id=id, user_id=request.user.id)
        if dislike.exists():
            dislike.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'users/password_reset_confirm.html'

    @method_decorator(sensitive_post_parameters('new_password1', 'new_password2'))
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(user=self.request.user)
        return context