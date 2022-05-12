from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from uuid import uuid4


# Create your models here.
class MyUser(AbstractUser):
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ('username', 'password')
    id = models.UUIDField(
            default=uuid4,
            unique=True,
            primary_key=True,
            editable=False
    )
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)


User = get_user_model()


class Category(models.Model):
    id = models.UUIDField(
            default=uuid4,
            unique=True,
            primary_key=True,
            editable=False
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name_plural = "categories"


class Note(models.Model):
    id = models.UUIDField(
            default=uuid4,
            unique=True,
            primary_key=True,
            editable=False
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=50)
    body = models.TextField(null=True, blank=True)
    is_pinned = models.BooleanField(default=False)
    category = models.ForeignKey(
            'Category',
            on_delete=models.SET_NULL,
            null=True,
            blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.title)


class Profile(models.Model):
    id = models.UUIDField(
            default=uuid4,
            unique=True,
            primary_key=True,
            editable=False
    )
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.username)
