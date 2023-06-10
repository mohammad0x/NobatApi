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
        profile_data = validated_data.pop('profile', None)
        if profile_data is not None:
            # We set address, assuming that you always set address
            # if you provide profile
            instance.profile.first_name = profile_data['first_name']
            instance.profile.last_name = profile_data['last_name']
            instance.profile.nationality_code = profile_data['nationality_code']
            instance.profile.phone = profile_data['phone']
            instance.profile.city = profile_data['city']
            instance.profile.address = profile_data['address']
            instance.profile.photo = profile_data['photo']
            # And save profile
            instance.profile.save()
        # Rest will be handled by DRF
        return super().update(instance, validated_data)

class CreateServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Create_Service
        fields = ['category', 'title', 'slug', 'image', 'edit']


class CreateServiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Create_Service
        fields = ('category', 'title', 'slug', 'image', 'edit')

    def update(self, instance, validated_data):
        # We try to get profile data
        # If we have one
        createService_data = validated_data.pop('createservice', None)
        if createService_data is not None:
            # We set address, assuming that you always set address
            # if you provide profile
            instance.createservice.category = createService_data['category']
            instance.createservice.title = createService_data['title']
            instance.createservice.slug = createService_data['slug']
            instance.createservice.image = createService_data['image']
            instance.createservice.edit = createService_data['edit']
            # And save profile
            instance.createservice.save()
        # Rest will be handled by DRF
        return super().update(instance, validated_data)

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['user','category', 'service', 'title', 'price', 'desc', 'active']

class ServiceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('category', 'service', 'title', 'price', 'desc', 'active')

    def update(self, instance, validated_data):
        Service_data = validated_data.pop('service', None)
        if Service_data is not None:
            instance.service.save()
        return super().update(instance, validated_data)

class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = ('user', 'service', 'busy', 'number', 'date', 'time')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('poster', 'image')

class CommentSerializer(serializers.ModelSerializer):
    # user = UserSerializer
    # HairStyle = CreateServiceSerializer
    class Meta:
        model = Comment
        fields = ('user', 'reply', 'HairStyle', 'rate', 'desc', 'date', 'is_reply')

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('image', 'user')

class DisLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisLike
        fields = ('image', 'user')