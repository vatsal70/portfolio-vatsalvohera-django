from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
import uuid
from django.dispatch import receiver
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
import random
import os
from django.dispatch import receiver
from cloudinary_storage.storage import RawMediaCloudinaryStorage, MediaCloudinaryStorage
import os
from django.dispatch import receiver
from ckeditor.fields import RichTextField
import cloudinary
# Create your models here.



class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, username, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, username, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, password, **extra_fields)
    




class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(error_messages={'unique': 'A user with that username already exists.'}, verbose_name='username', max_length=15, unique=True, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def get_absolute_url(self):
        return redirect("datapage")


        
        
class About(models.Model):
    about_text = models.CharField(max_length=2000, blank = True)
    img = models.ImageField(upload_to='about/', storage=MediaCloudinaryStorage())
    current = models.BooleanField(default = True)
    
    def __str__(self):
        return self.about_text[:10]
    
    class Meta:
        ordering = ('-id', )
    
    
class Skill(models.Model):
    skill_name = models.CharField(max_length = 20, blank = True)
    skill_percentage = models.CharField(max_length = 2, blank = True)
    
    def __str__(self):
        return self.skill_name
    
    class Meta:
        ordering = ('-id', )
    


class Project(models.Model):
    project_name = models.CharField(max_length = 200, blank = True)
    project_details = models.CharField(max_length = 2000, blank = True)
    project_link = models.CharField(max_length = 200, blank = True)
    
        
    def __str__(self):
        return self.project_name
        
    class Meta:
        ordering = ('-id', )
    
    
class Experience(models.Model):
    experience_type = models.CharField(max_length = 40, blank = True)
    experience_company = models.CharField(max_length = 200, blank = True)
    experience_duration = models.CharField(max_length = 200, blank = True)
    experience_details = RichTextField(max_length = 2000, blank=True, null=True)
    
    def __str__(self):
        return self.experience_company
    
    class Meta:
        ordering = ('-id', )
    
    
class Link(models.Model):
    link_name = models.CharField(max_length = 20, blank = True)
    link_url = models.URLField(max_length = 200)
    
    def __str__(self):
        return self.link_name
    
    class Meta:
        ordering = ('-id', )
        
    
class Contact(models.Model):
    contact_name = models.CharField(max_length=50, blank = True)
    contact_email = models.CharField(max_length=70, blank = True)
    contact_description = models.CharField(max_length=5000, blank = True)
    contact_replied = models.BooleanField(default = False)

    def __str__(self):
        return self.contact_email
    
    class Meta:
        ordering = ('-id', )
