from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import post_save
from django.utils import timezone
from django.forms import ModelForm
from jalali_date import datetime2jalali,date2jalali

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password, is_hair_style):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_hair_style=is_hair_style
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, is_hair_style=True):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
            is_hair_style=is_hair_style
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(unique=True,max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_hair_style = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="Profile")
    first_name = models.CharField(max_length=50, blank=True, null=False)
    last_name = models.CharField(max_length=50, blank=True, null=False)
    nationality_code = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    verify_code = models.CharField(max_length=4, blank=True, null=True)
    city = models.CharField(max_length=70, blank=True, null=False)
    address = models.CharField(max_length=200, blank=True, null=False)
    photo = models.ImageField(upload_to='profile_image/')


def save_profile_user(sender, **kwargs):
    if kwargs['created']:
        profile_user = Profile(user=kwargs['instance'])
        profile_user.save()


post_save.connect(save_profile_user, sender=MyUser)




class Category_createService(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_image/')
    status = models.BooleanField(default=True)
    position = models.IntegerField(null = True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title


class Category_Service(models.Model):
    services = models.ForeignKey(Category_createService, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='Category_Service/')
    status = models.BooleanField(default=True)
    position = models.IntegerField()

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title

