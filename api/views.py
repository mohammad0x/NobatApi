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

class createService(APIView):
    def get(self, request, id):
        data = Category_Service.objects.filter(services_id = id).values()
        return Response(data)
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

class UpdateUser(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()