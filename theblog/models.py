from django.db import models

#importing superuser we created
from django.contrib.auth.models import User

#To use this module     python -m pip install django-autoslug
from autoslug import AutoSlugField

#To send back to reverse url
from django.urls import reverse
from tinymce.models import HTMLField

#To use DateField we import
from datetime import date

#TO use ckeditor for rich text editor
#from django_ckeditor_5.fields import CKEditor5Field

from ckeditor.fields import RichTextField

#to do image resizes we use pip install pillow and then import Image from PIL
from PIL import Image,ImageChops


#----------------------------------------------------------------------------------------------------------------
class Category(models.Model):
    name=models.CharField(max_length=255)
    ct_slug=AutoSlugField(populate_from='name',unique=True,null=True,default=None)
    #ct_slug=models.SlugField(unique=True) #Custom Slugfield
    
    def save(self, *args, **kwargs):
        # Convert the name to lowercase before saving it
        self.name = self.name.lower()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog')
    
    #To show the name of Category model 'Categories' instead of 'categorys' in admin panel with 
    class Meta:
        verbose_name_plural = 'Categories'


#------------------------------------------------------------------------------------------------------------
class Post(models.Model):
    title=models.CharField(max_length=255)
    
    #first we need to install   pip install Pillow to upload images
    image=models.ImageField(upload_to="images/",null=True,blank=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    ingredients=RichTextField('Ingredients',blank=True,null=True)
    recipe=RichTextField('Recipe',blank=True,null=True)
    post_date=models.DateField(auto_now_add=True)
    category=models.CharField(max_length=255)    
    category_slug=AutoSlugField(populate_from='category',null=True,default=None)
    
    #Many to Many field allows us to associate different things to different tables
    likes=models.ManyToManyField(User,related_name='blog_posts')
    featured=models.BooleanField(default=False)

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        try:
            img=Image.open(self.image.path)
            size=(300,300)
            image_size=img.size
            
            if img.width >300 or img.height >300:
                #Calculate dimensions for cropping
                width,height=img.size
                new_width=min(width,height)
                new_height=new_width
                
                #crop the image
                left=(width-new_width)/2
                top=(height-new_height)/2
                right=(width+new_width)/2
                bottom=(height+new_height)/2
                img=img.crop((left,top,right,bottom))
            
            else:
                # Calculate the aspect ratio to maintain it
                width, height = img.size
                aspect_ratio = width / height
                if width<300:
                    new_width=300
                    new_height = int(new_width / aspect_ratio)
                
                if height<300:
                    new_height=300
                    new_width = int(new_height * aspect_ratio)
                                    
                 # Resize the image while maintaining the aspect ratio
                img = img.resize((new_width, new_height), Image.ANTIALIAS)
                
                 # Create a blank 300x300 square image
                final_img = Image.new("RGB", (300, 300), (255, 255, 255))

                # Calculate the position to center the resized image
                x = (300 - new_width) // 2
                y = (300 - new_height) // 2

                # Paste the resized image onto the blank square image
                final_img.paste(img, (x, y))
            
             
            # Save the cropped and resized image in its original format with quality 95
            img.save(self.image.path, quality=95)
                
        except Exception as e:
            pass    
        
            
    #To count no of likes on a post
    def total_likes(self):
        return self.likes.count()
        
    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
    
    #To get the values from form of html page
    def get_absolute_url(self):
        
        #reverse url to go to and argument passed as string of primary key(id) of this object
        return reverse('blog')    


#---------------------------------------------------------------------------------
class newsletterModel(models.Model):
    newsEmail=models.EmailField(max_length=100)

    def __str__(self):
        return self.newsEmail    

#-----------------------------------------------------------------------
class Profile(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    bio=models.TextField()
    profile_pic=models.ImageField(upload_to="images/profile/",null=True,blank=True)
    website_url=models.CharField(max_length=255,null=True,blank=True)
    facebook_url=models.CharField(max_length=255,null=True,blank=True)
    instagram_url=models.CharField(max_length=255,null=True,blank=True)
    twitter_url=models.CharField(max_length=255,null=True,blank=True)
    
    def __str__(self):
        return str(self.user)
    
    #To redirect to a url when form is submitted using this model   
    def get_absolute_url(self):        
        return reverse('home')    


#----------------------------------------------------------------------------
class Comment(models.Model):
    post=models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    body=models.TextField()
    date_added=models.DateField(auto_now_add=True)
    
    def __str__(self):
        #In admin portion we will see the title of post and the name of user who commented
        return '%s - %s' %(self.post.title,self.name)


#-------------------------------------------------------------------------------    
class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    mesg=models.TextField()
    
    def __str__(self):
        return str(self.name)