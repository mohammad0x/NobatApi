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

class Create_Service(models.Model):
    STATUS_CHOICES = (
        (1, 'one'),
        (2, 'two'),
        (3, 'three'),
        (4, 'four'),
        (5, 'five'),
    )
    category = models.ManyToManyField(Category_createService, related_name="Create_Services")
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="Create_Service")
    title = models.CharField(max_length=100, blank=False, null=False)
    slug = models.CharField(max_length=50)
    image = models.ImageField(upload_to='service_image/')
    score = models.CharField(max_length=5, choices=STATUS_CHOICES, blank=True)
    publish = models.DateTimeField(default=timezone.now)
    edit = models.BooleanField(default=False)




    def __str__(self):
        return self.title


def save_create_service(sender, instance, **kwargs):
    if kwargs['created'] and instance.is_hair_style == True:
        create_service = Create_Service.objects.create(user=instance)
        create_service.save()


post_save.connect(save_create_service, sender=MyUser)

class Service(models.Model):
    category = models.ForeignKey(Category_Service, on_delete=models.CASCADE, related_name='Service')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="Service")
    service = models.ForeignKey(Create_Service, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    desc = models.TextField()
    active = models.BooleanField(default=False)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Reserve(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='Reserves')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='Reserve')
    busy = models.BooleanField(default=False)
    number = models.IntegerField()
    date = models.CharField(max_length=10)
    time = models.TimeField()

    def __str__(self):
        return self.service.title

    def get_jalali_date(self):
        return datetime2jalali(self.date)

class Image(models.Model):
    poster = models.ForeignKey(Create_Service, on_delete=models.CASCADE, related_name='post')
    image = models.ImageField(upload_to='pos_image/')

class Like(models.Model):
    user = models.ForeignKey(MyUser, on_delete= models.CASCADE, null=True, blank=True, related_name='user_like')
    image = models.ForeignKey(Image, on_delete= models.CASCADE, null=True, blank=True, related_name='image_like')

class DisLike(models.Model):
    user = models.ForeignKey(MyUser, on_delete= models.CASCADE, null=True, blank=True, related_name='user_dislike')
    image = models.ForeignKey(Image, on_delete= models.CASCADE, null=True, blank=True, related_name='image_dislike')

class Comment(models.Model):
    user = models.ForeignKey(MyUser, related_name='user', on_delete=models.CASCADE)
    reply = models.ForeignKey("self", related_name='commentid', on_delete=models.CASCADE, blank=True, null=True)
    HairStyle = models.ForeignKey(Create_Service, related_name='post_key', on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(default=1)
    desc = models.TextField(max_length=700)
    date = models.DateTimeField(default=timezone.now)
    is_reply = models.BooleanField(default=False)

    def __str__(self):
        return self.post_key.title

class comment_form(ModelForm):
    class Meta:
        model = Comment
        fields = ['desc', 'rate']
class reply_form(ModelForm):
    class Meta:
        model = Comment
        fields = ['desc']