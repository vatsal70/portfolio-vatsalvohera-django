"""portfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import admin_experience


admin.site.site_header = 'Vatsal Vohera Portfolio - Admin'
admin.site.site_title = 'Vatsal Vohera PortfolioStudent-Teacher Portal - Title'
admin.site.index_title = 'Welcome to Portfolio Admin - Admin Panel'


urlpatterns = [
    path('', views.homepage, name = 'homepage'),
    path('admin/', admin.site.urls),
    path('login_page/', views.login_request, name = 'login_page'),
    path('logout_request/', views.logout_request, name = 'logout_request'),
    
    
    
    #homepage for admin section
    path('admin_page/', views.admin_page, name = 'admin_page'),
    path('authentication_required/', views.authentication_required, name = "authenticationRequired"),
    
    
    
    #about page urls for admin
    path('admin_about/', views.admin_about, name = 'admin_about'),
    path('admin_about_edit/<about_id>', views.admin_about_edit, name = 'admin_about_edit'),
    path('admin_about_delete/<about_id>', views.admin_about_delete, name = 'admin_about_delete'),
    path('admin_change_current_about/<about_id>', views.admin_change_current_about, name = 'admin_change_current_about'),
    
    #skills page urls for admin
    path('admin_skill/', views.admin_skill, name = 'admin_skill'),
    path('admin_skill_edit/<skill_id>', views.admin_skill_edit, name = 'admin_skill_edit'),
    path('admin_skill_delete/<skill_id>', views.admin_skill_delete, name = 'admin_skill_delete'),
    
    
    #project page urls for admin
    path('admin_project/', views.admin_project, name = 'admin_project'),
    path('admin_project_edit/<project_id>', views.admin_project_edit, name = 'admin_project_edit'),
    path('admin_project_delete/<project_id>', views.admin_project_delete, name = 'admin_project_delete'),
    
    
    #experience page urls for admin
    path('admin_experience/', admin_experience.as_view(), name = 'admin_experience'),
    path('admin_experience_edit/<work_id>', views.admin_experience_edit, name = 'admin_experience_edit'),
    path('admin_experience_delete/<work_id>', views.admin_experience_delete, name = 'admin_experience_delete'),
    
    #contact page urls for admin
    path('admin_contact_message/', views.admin_contact_message, name = 'admin_contact_message'),
    path('admin_contact_page/', views.admin_contact_page, name = 'admin_contact_page'),
    path('admin_contact_delete/<contact_id>', views.admin_contact_delete, name = 'admin_contact_delete'),
    path('admin_contact_reply/<contact_id>', views.admin_contact_reply, name = 'admin_contact_reply'),
    
    
    #links page urls for admin
    path('admin_link/', views.admin_link, name = 'admin_link'),
    path('admin_link_edit/<link_id>', views.admin_link_edit, name = 'admin_link_edit'),
    path('admin_link_delete/<link_id>', views.admin_link_delete, name = 'admin_link_delete'),
    

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'portfolio.views.error_404_view'