from django.contrib.auth.forms import UserCreationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from theblog.models import Profile

Users=Profile.objects.all()
# Create a list of choices in the format required for a form field
user_list = [(Profile.user, Profile.user) for user in Users]



class SignUpForm(UserCreationForm):
    email=forms.EmailField(max_length=100,widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta: 
        model=User
        fields=('username','first_name','last_name','email','password1','password2')
      
    def __init__(self,*args,**kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)
        
        self.fields['username'].widget.attrs['class']='form-control mb-3'
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['class']='form-control'
        
        
        
        
class EditProfileForm(UserChangeForm):
    email=forms.EmailField(max_length=100,widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_login=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    is_superuser=forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    is_staff=forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    is_active=forms.CharField(max_length=100,widget=forms.CheckboxInput(attrs={'class':'form-check'}))
    date_joined=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
        
    class Meta: 
        model=User
        fields=('username','first_name','last_name','email','password','last_login','date_joined','is_superuser','is_staff','is_active')

    #def __init__(self, *args, **kwargs):
     #   super(EditProfileForm, self).__init__(*args, **kwargs)
        
        # Remove fields you don't want to display
        #del self.fields['date_joined','is_active','is_staff','is_superuser','last_login']

    

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password1=forms.CharField(max_length=100,label='New Password',widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password2=forms.CharField(max_length=100,label='Confirm New Password',widget=forms.PasswordInput(attrs={'class':'form-control','type':'password','label':'Confirm Password'})) 
     
            
    class Meta:
        model = User
        fields = ('old_password', 'password','confirmpassword')
        
class ProfilePageForm(forms.ModelForm):
    profile_pic=forms.ImageField(label='Upload Profile Pic',
                                 required=False,
                                 widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),)
    
    class Meta:
        model=Profile
        fields = ("bio","profile_pic","website_url","facebook_url","instagram_url","twitter_url")
        
        #To style our form
        widgets={
            'bio':forms.Textarea(attrs={'class':'form-control'}),        
            'website_url':forms.TextInput(attrs={'class':'form-control','placeholder':'Website'}),
            'facebook_url': forms.TextInput(attrs={'class':'form-control','placeholder':'Facebook'}),
            'instagram_url':forms.TextInput(attrs={'class':'form-control','placeholder':'Instagram'}),
            'twitter_url':forms.TextInput(attrs={'class':'form-control','placeholder':'Twitter'}),
        }



