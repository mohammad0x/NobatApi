from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUser.objects.create_user(validated_data['email'], validated_data['username'], validated_data['password'],is_hair_style=False)

        return user

class RegisterSerializerHair(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUser.objects.create_user(validated_data['email'], validated_data['username'], validated_data['password'],is_hair_style=True)

        return user

class Category_createServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category_createService
        fields = ('title', 'status', 'image')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'nationality_code', 'phone', 'city', 'address', 'photo')

class ProfileUppdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'nationality_code', 'phone', 'city', 'address', 'photo')

    def update(self, instance, validated_data):
        # We try to get profile data
        # If we have one
        profile = Profile
        print(profile)
        if profile is not None:
            # We set address, assuming that you always set address
            # if you provide profile
            instance.profile.first_name = profile['first_name']
            instance.profile.last_name = profile['last_name']
            instance.profile.nationality_code = profile['nationality_code']
            instance.profile.phone = profile['phone']
            instance.profile.city = profile['city']
            instance.profile.address = profile['address']
            instance.profile.photo = profile['photo']
            # And save profile
            instance.profile.save()
        # Rest will be handled by DRF
        return super().update(instance, validated_data)

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['user','category', 'service', 'title', 'price', 'desc', 'active']