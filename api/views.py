from django.core import serializers
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import *
from rest_framework.renderers import JSONRenderer
from .models import MyUser
from django.http import JsonResponse
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

# add

class categoryCreateService(APIView):

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

class ListCategoryCreateService(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        """
        Return a list of all users.

        """
        from django.core import serializers

        # content = serializers.serialize("json", Category_createService.objects.filter(status=True).values())
        content = Category_createService.objects.filter(status=True).values()
        return Response(content,status=status.HTTP_200_OK)
