from django.forms import ModelForm
from django import forms
from PIL import Image
from .models import Post,Category,Comment
#from ckeditor.widgets import RichTextField
#from django_ckeditor_5.widgets import CKEditor5Widget

#If we hardcode the values of choices added in categories field
#cats=[('Deserts','Deserts'),('Desi cuisine','Desi cuisine'),('Fast food','Fast food')]

# Retrieve all categories from the database
categories = Category.objects.all()

# Create a list of choices in the format required for a form field
choice_list = [(category.name, category.name) for category in categories]

# Convert values to title case
choice_list = [(value, label.title()) for value,label in choice_list]

class PostForm(forms.ModelForm):
    image = forms.ImageField(label='Upload Image',
    #help_text='Max size: 2 MB',
    required=False,  # Set to True if the field is required
    widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    
    
    class Meta:
        model=Post
        fields = ("title","author","category","ingredients","recipe","image","featured")
            
        #To style our form
        widgets={
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}),
            'author':forms.TextInput(attrs={'class':'form-control','value':'','id':'elder','type':'hidden' }),
            'category': forms.Select(choices=choice_list,attrs={'class':'form-control'}),
            'ingredients':forms.Textarea(attrs={'class':'form-control'}),
            'recipe':forms.Textarea(attrs={'class':'form-control'}),
            
        }
        
    def clean_image(self):
        cimage=self.cleaned_data['image']
        
        if cimage:
             # Open the image and check its dimensions
            img = Image.open(cimage)

            # Check if both width and height are greater than 300 pixels
            if img.width < 300 or img.height < 300:
                raise forms.ValidationError("Image dimensions must be greater than 300x300 pixels.")
        return cimage   
    

            
class EditForm(forms.ModelForm):

    class Meta:
        model=Post
        fields = ("title","author","category","ingredients","recipe","image","featured")
        
        #To style our form
        widgets={
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Title'}),
            'author':forms.TextInput(attrs={'class':'form-control','value':'','id':'elder','type':'hidden' }),
            'category': forms.Select(choices=choice_list,attrs={'class':'form-control'}),
            'ingredients':forms.Textarea(attrs={'class':'form-control'}),
            'recipe':forms.Textarea(attrs={'class':'form-control'}),
            'image':forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
 
    def clean_image(self):
        cimage=self.cleaned_data['image']
        
        if cimage:
             # Open the image and check its dimensions
            img = Image.open(cimage)

            # Check if both width and height are greater than 300 pixels
            if img.width < 300 or img.height < 300:
                raise forms.ValidationError("Image dimensions must be greater than 300x300 pixels.")
        return cimage   
    
class CategoryForm(forms.ModelForm): 
    
    class Meta:
        model=Category
        fields= ("name",)
         
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
        }
        
