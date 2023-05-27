import json
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
        serializer = Category_createServiceSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class categoryCreate(APIView):
    def get(self, request, id):
        data = get_object_or_404(Category_Service, id = id,status=True)

        return JsonResponse({
            'id':data.id,
            'title':data.title,
            'image':data.image.url,
            'status':data.status,
            'position':data.position,
        },status=status.HTTP_200_OK)
class ProfileView(APIView):
    def get(self, request ):
        profile = Profile.objects.get(user_id=request.user.id)

        return JsonResponse({
            'id':profile.id,
            'first_name':profile.first_name,
            'last_name':profile.last_name,
            'nationality_code':profile.nationality_code,
            'phone':profile.phone,
            'verify_code':profile.verify_code,
            'city':profile.city,
            'address':profile.address,
            'photo':profile.photo.url,
        },status=status.HTTP_200_OK)

class UpdateProfile(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

class createService(APIView):
    serializer_class = CreateServiceSerializer
    def post(self, request, id, *args, **kwargs,):
        data = {
            'category': request.data.get('category'),
            'user': request.data.get(id),
            'title': request.data.get('title'),
            'slug': request.data.get('slug'),
            'image': request.data.get('image'),
        }
        serializer = CreateServiceSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)