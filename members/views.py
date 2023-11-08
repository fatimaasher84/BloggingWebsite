from django.shortcuts import render,get_object_or_404
from django.views import generic
#from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SignUpForm,EditProfileForm,CustomPasswordChangeForm,ProfilePageForm
from django.views.generic import DetailView,CreateView

from theblog.models import Profile,Post


#------------------------------------------------------------------
class CreateProfilePageView(CreateView):
    model=Profile
    form_class=ProfilePageForm
    template_name='registration/create_profile_page.html'
    success_url=reverse_lazy('home')
    posts=Post.objects.all().order_by('-id')[:2]
    
    #Allows django to know which user is creating profile page
    def form_valid(self,form):
        #tells which user is filling the form save that  user
        form.instance.user=self.request.user
        return super().form_valid(form)

#-----------------------------------------------------------------
class EditProfilePageView(generic.UpdateView):
    model=Profile
    form_class=ProfilePageForm
    template_name='registration/edit_profile_page.html'
    #fields=['bio','profile_pic','website_url','facebook_url','instagram_url','twitter_url']
    success_url=reverse_lazy('home')
    
    def get_context_data(self,*args, **kwargs):
        context = super(EditProfilePageView,self).get_context_data(*args,**kwargs)
        posts=Post.objects.all().order_by('-id')[:2]
        context['posts']=posts
        return context
#-----------------------------------------------------------------
class ShowProfilePageView(DetailView):
    model=Profile
    template_name='registration/user_profile.html'
    context_object_name='page_user'
    success_url=reverse_lazy('article-detail')
    
    def get_context_data(self,*args, **kwargs):
        #users=Profile.objects.all() 
        context = super(ShowProfilePageView,self).get_context_data(*args,**kwargs)
        page_user=get_object_or_404(Profile,id=self.kwargs['pk'])
        posts=Post.objects.all().order_by('-id')[:2]
        context['posts']=posts
        context['page_user']=page_user
        return context
    



#----------------------------------------------------------------
class UserRegisterView(CreateView):
    form_class=SignUpForm
    template_name='registration/register.html'
    success_url=reverse_lazy('login')
    
    def get_context_data(self,*args, **kwargs):
        context = super(UserRegisterView,self).get_context_data(*args,**kwargs)
        posts=Post.objects.all().order_by('-id')[:2]
        context['posts']=posts
        return context

#----------------------------------------------------------------
class UserEditView(generic.UpdateView):
    form_class=EditProfileForm
    template_name='registration/edit_profile.html'
    success_url=reverse_lazy('home')
    
    def get_object(self):
        return self.request.user

    def get_context_data(self,*args, **kwargs):
        context = super(UserEditView,self).get_context_data(*args,**kwargs)
        posts=Post.objects.all().order_by('-id')[:2]
        context['posts']=posts
        return context
#----------------------------------------------------------------
class PasswordsChangeView(PasswordChangeView):
    form_class=CustomPasswordChangeForm
    template_name='registration/change-password.html'
    success_url=reverse_lazy('password_success')
    
    def get_context_data(self,*args, **kwargs):
        #user=Profile.objects.all() 
        context = super(PasswordsChangeView,self).get_context_data(**kwargs)
        #page_user=get_object_or_404(Profile,id=self.kwargs['pk'])
        #context['page_user']=page_user
        posts=Post.objects.all().order_by('-id')[:2]
        context['posts']=posts
        return context

    def get_object(self):
       return self.request.user


#---------------------------------------------------------------
def password_success(request):
    posts=Post.objects.all().order_by('-id')[:2]
    return render(request,"registration/password_success.html",{'posts':posts})



    