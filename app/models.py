from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from app.managers import CustomUserManager


# Create your models here.


class Event(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images')

    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Events"
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


class Member(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Members"
        ordering = ('-created_at',)

    def __str__(self):
        return self.full_name


class People(models.Model):
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.email


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []


class Contact(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)

    def str(self):
        return self.full_name
