from django.urls import path
from . import views
from .views import UserRegisterView,UserEditView,PasswordsChangeView,ShowProfilePageView,EditProfilePageView,CreateProfilePageView


#To handle password change page provided by django authentication system,we need to use auth_view
#from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',UserRegisterView.as_view(),name='register'),
    path('edit_profile/',UserEditView.as_view(),name='edit_profile'),
    path('password/',PasswordsChangeView.as_view(),name="password_change"),
    path('password_success/',views.password_success,name="password_success"),
    path('<int:pk>/profile/',ShowProfilePageView.as_view(),name="show_profile_page"),
    path('<int:pk>/edit_profile_page/',EditProfilePageView.as_view(),name="edit_profile_page"),
    path('create_profile_page/',CreateProfilePageView.as_view(),name="create_profile_page"),
    
]
