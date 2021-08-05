from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.decorators import user_passes_test, login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from backend.models import *
from backend.forms import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from backend.task import *
from ckeditor.fields import RichTextField
from .decorators import *
from django.template.loader import render_to_string








def homepage(request):
    params = {}
    try:
        try:
            if not About.objects.filter(current = True):
                latest = About.objects.latest('id')
                latest.current = True
                latest.save()
                print("yess")
            about = About.objects.filter(current = True)[0]
            params['about'] = about
        except Exception as e:
            print(e)
        try:
            skills = Skill.objects.all()
            params['skills'] = skills
        except Exception as e:
            print(e)
        try:
            project = Project.objects.all()
            params['project'] = project
        except Exception as e:
            print(e)
        try:
            experience = Experience.objects.all()
            params['experience'] = experience
        except Exception as e:
            print(e)
        try:
            link = Link.objects.all()
            params['link'] = link
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
    return render(request, 'frontend/index.html', params)




@login_required(login_url='/authentication_required/')
@active_user_required
def admin_page(request):
    return render(request, 'frontend/admin.html')








@login_required(login_url='/authentication_required/')
@active_user_required
def admin_about(request):
    about_model = About.objects.all()
    if request.method == "POST":
        about_text = request.POST.get('about_text')
        img = request.FILES.get('img')
        about = About(about_text=about_text, img=img)
        about.save()
        latest_id = About.objects.latest('id').id
        make_all_aboutitem_false_except.delay(latest_id)
        return redirect('admin_about')
    params = {
        'about_model': about_model,
        'about_page': True
    }
    return render(request, 'frontend/admin_about.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_about_edit(request, about_id):
    instance = get_object_or_404(About, id = about_id)
    old_image = str(instance.img)
    form = EditAboutProfile(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        remove_file_from_cloudinary.delay(old_image)
        return redirect('admin_about')
    params = {
        'form': form
        }
    return render(request, 'frontend/admin_about.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_about_delete(request, about_id):
    instance = get_object_or_404(About, id = about_id)
    old_image = str(instance.img)
    instance.delete()
    try:
        latest_about = About.objects.latest('id')
        latest_id = latest_about.id
        remove_file_from_cloudinary.delay(old_image)
        make_all_aboutitem_false_except.delay(latest_id)
        latest_about.current = True
        latest_about.save()
    except Exception as e:
        print(e)
    params = {
        'about_page': True
    }
    return redirect('admin_about')



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_change_current_about(request, about_id):
    about = About.objects.all()
    our_about = about.get(id = about_id)
    about_id_celery = our_about.id
    make_all_aboutitem_false_except.delay(about_id_celery)
    our_about.current = True
    our_about.save()
    params = {
        'about_page': True
    }
    return redirect('admin_about')
    



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_skill(request):
    skill_model = Skill.objects.all()
    if request.method == "POST":
        skill_name = request.POST.get('skill_name')
        skill_percentage = request.POST.get('skill_percentage')
        skill = Skill(skill_name=skill_name, skill_percentage=skill_percentage)
        skill.save()
        return redirect('admin_skill')
    params = {
        'skill_model': skill_model,
        'skill_page': True
    }
    return render(request, 'frontend/admin_skill.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_skill_edit(request, skill_id):
    instance = get_object_or_404(Skill, id = skill_id)
    form = EditSkillProfile(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('admin_skill')
    params = {
        'form': form
        }
    return render(request, 'frontend/admin_skill.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_skill_delete(request, skill_id):
    instance = get_object_or_404(Skill, id = skill_id)
    instance.delete()
    params = {
        'skill_page': True
    }
    return redirect('admin_skill')




@login_required(login_url='/authentication_required/')
@active_user_required
def admin_project(request):
    project_model = Project.objects.all()
    if request.method == "POST":
        project_name = request.POST.get('project_name')
        project_details = request.POST.get('project_details')
        project_link = request.POST.get('project_link')
        project = Project(project_name=project_name, project_details=project_details, project_link=project_link)
        project.save()
        return redirect('admin_project')
    params = {
        'project_model': project_model,
        'project_page': True
    }
    return render(request, 'frontend/admin_project.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_project_edit(request, project_id):
    instance = get_object_or_404(Project, id = project_id)
    form = EditProjectProfile(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('admin_project')
    params = {
        'form': form
        }
    return render(request, 'frontend/admin_skill.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_project_delete(request, project_id):
    instance = get_object_or_404(Project, id = project_id)
    instance.delete()
    params = {
        'project_page': True
    }
    return redirect('admin_project')




from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
class admin_experience(LoggedInRedirectMixin, CreateView):
    model = Experience
    template_name = 'frontend/admin_experience.html'
    form_class = EditExperienceProfile
    success_url = reverse_lazy('admin_experience')
    
    def get_context_data(self, *args, **kwargs):
        experience_model = Experience.objects.all()
        params = super(admin_experience, self).get_context_data(*args, **kwargs)
        params["experience_model"] = experience_model
        params["experience_page"] = True
        return params



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_experience_edit(request, work_id):
    instance = get_object_or_404(Work, id = work_id)
    form = EditExperienceProfile(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('admin_experience')
    params = {
        'form': form
        }
    return render(request, 'frontend/admin_experience.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_experience_delete(request, work_id):
    instance = get_object_or_404(Experience, id = work_id)
    instance.delete()
    params = {
        'work_page': True
    }
    return redirect('admin_experience')




@login_required(login_url='/authentication_required/')
@active_user_required
def admin_contact_message(request):
    if request.method == "POST":
        contact_name = request.POST.get('contact_name')
        contact_email = request.POST.get('contact_email')
        contact_description = request.POST.get('contact_description')
        contact = Contact(contact_name=contact_name, contact_email=contact_email, contact_description=contact_description)
        contact.save()
        return redirect('homepage')



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_contact_page(request):
    contact_model = Contact.objects.all()
    params = {
        'contact_model': contact_model,
        'contact_page': True,
    }
    return render(request, 'frontend/admin_contact_page.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_contact_reply(request, contact_id):
    instance = get_object_or_404(Contact, id = contact_id)
    contact_email = instance.contact_email
    contact_description = instance.contact_description
    if request.method == "POST":
        contact_email_get = request.POST.get('contact_email_get')
        contact_description_get = request.POST.get('contact_description_get')
        contact_reply_get = request.POST.get('contact_reply_get')
        # print("contact_email_get", contact_email_get)
        # print("contact_description_get", contact_description_get)
        # print("contact_reply_get", contact_reply_get)
        email_template_name = "frontend/reply_mail.txt"
        c = {
             'contact_email_get' : contact_email_get,
             'contact_description_get' : contact_description_get,
             'contact_reply_get' : contact_reply_get,
             }
        email_body = render_to_string(email_template_name, c)
        send_mail_task.delay('Reply', email_body,   
             contact_email_get,
             contact_id,
            )
        return redirect('admin_contact_page')
    params = {
        'contact_email': contact_email,
        'contact_description': contact_description,
        }
    return render(request, 'frontend/admin_contact_page.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_contact_delete(request, contact_id):
    instance = get_object_or_404(Contact, id = contact_id)
    instance.delete()
    params = {
        'contact_page': True
    }
    return redirect('admin_contact_page')



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_link(request):
    link_model = Link.objects.all()
    if request.method == "POST":
        link_name = request.POST.get('link_name')
        link_url = request.POST.get('link_url')
        link = Link(link_name=link_name, link_url=link_url)
        link.save()
        return redirect('admin_link')
    params = {
        'link_model': link_model,
        'link_page': True,
    }
    return render(request, 'frontend/admin_link.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_link_edit(request, link_id):
    instance = get_object_or_404(Link, id = link_id)
    form = EditLinkProfile(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('admin_link')
    params = {
        'form': form
        }
    return render(request, 'frontend/admin_link.html', params)



@login_required(login_url='/authentication_required/')
@active_user_required
def admin_link_delete(request, link_id):
    instance = get_object_or_404(Link, id = link_id)
    instance.delete()
    params = {
        'link_page': True
    }
    return redirect('admin_link')




def logout_request(request):
    logout(request)
    print("Logged out successfully!")
    return redirect("/")


def login_request(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('admin_page')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            username = request.POST.get('email')
            password = request.POST.get('password')
            user_exists = User.objects.filter(email=username).exists()
            if user_exists:
                try:
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}")
                    print("You are now logged in as", username)
                    return redirect('admin_about')
                except:
                    errors = "Incorrect Password"
                    print("Incorrect Password")
                    context['errors'] = errors
            else:
                print("username does not exists.")
                errors = "Username/Email does not exists."
                context['errors'] = errors
        form = AuthenticationForm()
        context['form'] = form
    return render(request, "frontend/login.html", context)




def error_404_view(request, exception):
    data = {
        "error": "404",
        "message": "The page you requested was not found."
        }
    return render(request, 'frontend/login_required.html', data)


