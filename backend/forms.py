from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import *
from django.db import models
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import HttpResponse
from django.forms import ModelChoiceField
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext_lazy as _








class EditAboutProfile(forms.ModelForm):
    about_text = forms.CharField(max_length = 2000, required=False, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }),
                                 )
    img = forms.ImageField()
    
    class Meta:
        model = About
        fields = ('about_text', 'img')
        
        
        

class EditSkillProfile(forms.ModelForm):
    skill_name = forms.CharField(max_length = 20, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Skill"
                                 )
    skill_percentage = forms.CharField(max_length = 2, required=False, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Percentage"
                                 )
    
    class Meta:
        model = Skill
        fields = ('skill_name', 'skill_percentage')
        
class EditProjectProfile(forms.ModelForm):
    project_name = forms.CharField(max_length = 200, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Project")
    project_details = forms.CharField(max_length = 2000, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Details")
    project_link = forms.CharField(max_length = 200,widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Link")
    
    class Meta:
        model = Project
        fields = ('project_name', 'project_details', 'project_link')
        
        
        
class EditExperienceProfile(forms.ModelForm):
    experience_type = forms.CharField(max_length = 40, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Type"
                                 )
    experience_company = forms.CharField(max_length = 200, required=False, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Company"
                                 )
    experience_duration = forms.CharField(max_length = 200, 
                                 widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Duration"
                                 )
    
    class Meta:
        model = Experience
        fields = ('experience_type', 'experience_company','experience_duration', 'experience_details')



class EditLinkProfile(forms.ModelForm):
    link_name = forms.CharField(max_length = 200, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="Name")
    link_url = forms.URLField(max_length = 2000, widget = forms.TextInput(
                                     attrs={
                                         'class': 'form-control'
                                         }), label="URL")
    
    class Meta:
        model = Link
        fields = ('link_name', 'link_url')