#get_object_or_404 is used to get an object if it exists,if it doesnot exist give a 404 error
from typing import Any
from django.db import models
from django.shortcuts import render,get_object_or_404
from .models import Post,Category,newsletterModel,Comment,Contact

from .forms import PostForm,EditForm,CategoryForm

#To use class based views(ListView makes a query set and store it in database and then show in the form of list)
#(DetailView makes a query set and store it in database and then show detail of one record from list)
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
import os 

from django.templatetags.static import static

#To use paginator
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from PIL import Image

#Function Based View
def HomeView(request):    
    
    image_files=Post.objects.filter(featured='True')
    # Path to the directory containing the images
    image_folder = 'images/slider/'
    image_folder_path=os.path.join('static', 'images', 'slider')
    image_extensions=('.jpg','.jpeg','.gif','.png')
    imagefiles=[]

    try:
        # List image files in the directory
        imagefiles = [image_folder + filename for filename in os.listdir(image_folder_path) if filename.lower().endswith(image_extensions)]
    except FileNotFoundError:
        # Handle the case where the directory does not exist or is empty
        pass
    
    #all the categories
    cat_menu=Category.objects.all()
    #Will display only two last added blog posts
    posts=Post.objects.all().order_by('-id')[:2]    
    
    context={
        'cat_menu':cat_menu,
        'imagefiles':imagefiles,
        'image_files':image_files,
        'image_folder':image_folder,
        'posts':posts
        }
    return render(request,'index.html',context) 



#------------------------------------------------------------
def footerView(request):
    
    return render(request,'footer.html',{}) 



#------------------------------------------------------------    
def CategoryView(request, slug):
    try:
        cat_menu=Category.objects.all()
        category_name = slug.replace('-',' ')
        category_posts = Post.objects.filter(category_slug=slug)
        posts=Post.objects.all().order_by('-id')[:2]
        categoryData=Post.objects.all().order_by('-post_date')
        paginator=Paginator(categoryData,3)
        page_number=request.GET.get('page')
        categoryDataFinal=paginator.get_page(page_number)
        totalpage=categoryDataFinal.paginator.num_pages
    
    
        context= {
            'categoryData':categoryDataFinal,
            'lastpage':totalpage,
            'totalPageList':[n+1 for n in range(totalpage)],
            'category_posts': category_posts,
            'cats': category_name,
            'cat_menu':cat_menu,
            'posts':posts,
            'slug':slug
        }
        return render(request, 'categories.html',context) 
    except Exception as e:
        print(f"Error: {e}")


    
#------------------------------------------------------------    
def CategoryListView(request):
    try:
       cat_menu_list=Category.objects.all()       
       posts=Post.objects.all().order_by('-id')[:2]
       return render(request,'category_list.html',{'cat_menu_list':cat_menu_list,'posts':posts}) 
    
    except Exception as e:
        print(e)


#------------------------------------------------------------    
def LikeView(request,pk):
    #The post_id given in form submit button is now looked up in Post Model
    post=get_object_or_404(Post,id=request.POST.get('post_id'))
    liked=False
    posts=Post.objects.all().order_by('-id')[:2]
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked=False
    else:
        #To save the like in post model with the user name who liked it 
        post.likes.add(request.user)
        liked=True
    
    #We dont want to redirect to another page instead we want to stay on the same page after liking the post
    return HttpResponseRedirect(reverse('article-detail',args=[str(pk)]))#args will tell which post to redirect to and args take string value 
    

    
#------------------------------------------------------------    
#Class Based Views
class ArticleDetailView(DetailView):
    model=Post
    template_name='article_details.html'

    def get_context_data(self,*args, **kwargs):
        cat_menu=Category.objects.all() 
        context = super(ArticleDetailView,self).get_context_data(**kwargs)
        context['cat_menu']=cat_menu
        context['ingredients'] = self.get_object().ingredients
        # Access the HTML field of the model and include it in the context
        context['html_content'] = self.get_object().recipe  # Assuming 'html_content' is the HTML field
        
        #To note down which post we are on
        stuff=get_object_or_404(Post,id=self.kwargs['pk'])
        total_likes=stuff.total_likes()#total_likes is a function 
        posts=Post.objects.all().order_by('-id')[:2]
        sorted_comments = stuff.comments.all().order_by('-date_added')

        liked=False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked=True
        context['total_likes']=total_likes
        context['posts']=posts
        context['liked']=liked
        context['sorted_comments']=sorted_comments
        return context
    
    

#------------------------------------------------------------
class AddPostView(CreateView):
    form_class=PostForm
    template_name='add_post.html'
    
    
    def form_valid(self,form):
        # Get the uploaded image from the form
        image = form.cleaned_data['image']

        if image:
            # Open the image and check its dimensions
            img = Image.open(image)

            # Check if both width and height are greater than 300 pixels
            if img.width < 300 or img.height < 300:
                form.add_error('image','Image dimensions must be greater than 300x300 pixels.')
                return self.form_invalid(form)
            
        return super().form_valid(form)        
            
    def get_context_data(self,*args, **kwargs):
        cat_menu=Category.objects.all() 
        posts=Post.objects.all().order_by('-id')[:2]
        context = super(AddPostView,self).get_context_data(**kwargs)
        context['cat_menu']=cat_menu
        context['posts']=posts
        return context
        
    
        


#-----------------------------------------------------------------
class AddCategoryView(CreateView):
    model=Category
    form_class=CategoryForm
    template_name='add_category.html'
    #fields='__all__'

    def get_context_data(self,*args, **kwargs):
        cat_menu=Category.objects.all() 
        context = super(AddCategoryView,self).get_context_data(**kwargs)
        posts=Post.objects.all().order_by('-id')[:2]
        context['cat_menu']=cat_menu
        context['posts']=posts
        return context
    

#------------------------------------------------------------
class UpdatePostView(UpdateView):
    model=Post
    form_class=EditForm
    template_name='update_post.html'
    
    def form_valid(self,form):
        # Get the uploaded image from the form
        image = form.cleaned_data['image']

        if image:
            # Open the image and check its dimensions
            img = Image.open(image)

            # Check if both width and height are greater than 300 pixels
            if img.width < 300 or img.height < 300:
                form.add_error('image','Image dimensions must be greater than 300x300 pixels.')
                return self.form_invalid(form)
            
        return super().form_valid(form)        
    
    def get_context_data(self,*args, **kwargs):
        cat_menu=Category.objects.all()
        posts=Post.objects.all().order_by('-id')[:2] 
        context = super(UpdatePostView,self).get_context_data(**kwargs)
        context['cat_menu']=cat_menu
        context['posts']=posts
        return context
    

#------------------------------------------------------------
class DeletePostView(DeleteView):
    model=Post
    template_name='delete_post.html'
    
    #This is used to send to home page after deleting
    success_url=reverse_lazy('blog')    

    def get_context_data(self,*args, **kwargs):
        cat_menu=Category.objects.all()
        posts=Post.objects.all().order_by('-id')[:2] 
        context = super(DeletePostView,self).get_context_data(**kwargs)
        context['cat_menu']=cat_menu
        context['posts']=posts
        return context
    

#------------------------------------------------------------
def AboutView(request):
    cat_menu=Category.objects.all() 
    posts=Post.objects.all().order_by('-id')[:2]
    context={
        'cat_menu':cat_menu,
        'posts':posts
    }
    return render(request,"about.html",context)
    

#------------------------------------------------------------
def BlogView(request):
    blogData=Post.objects.all().order_by('-post_date')
    paginator=Paginator(blogData,3)
    page_number=request.GET.get('page')
    blogDataFinal=paginator.get_page(page_number)
    totalpage=blogDataFinal.paginator.num_pages
    
    cat_menu=Category.objects.all()
    posts=Post.objects.all().order_by('-id')[:2]
    #html_contents=posts.recipe
    data={
        'blogData':blogDataFinal,
        'lastpage':totalpage,
        'totalPageList':[n+1 for n in range(totalpage)],
        'cat_menu':cat_menu,
        'posts':posts,
    #    'html_contents':html_contents
    }
        
    return render(request,"blog.html",data)

""" class BlogView(ListView):
    model = Post
    template_name='blog.html'
    context_object_name='blogData'
    #TO order posts by date created
    ordering=['-post_date']
    paginate_by=3 #No of items per page
    
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        cat_menu=Category.objects.all()
        posts=Post.objects.all().order_by('-id')[:2]
        context['cat_menu']=cat_menu
        context['posts']=posts
        # Access the HTML field of each model instance and include them in the context
        context['html_contents'] = [post.recipe for post in context['blogData']]  # Assuming 'recipe' is the HTML field
        
        # Calculate pagination manually
        paginator = Paginator(context['blogData'], self.paginate_by)
        page = self.request.GET.get('page')
        context['blogData'] = paginator.get_page(page)
        context['lastpage']=context['blogData'].paginator.num_pages
         
        
        return context
 """

#------------------------------------------------------------
def NewsView(request):
    cat_menu=Category.objects.all()
    posts=Post.objects.all().order_by('-id')[:2] 
    context={
        'cat_menu':cat_menu,
        'posts':posts
    }
    return render(request,"news.html",context)

#------------------------------------------------------------
def ContactView(request):  
    cat_menu=Category.objects.all() 
    posts=Post.objects.all().order_by('-id')[:2]
    context={
        'cat_menu':cat_menu,
        'posts':posts
    }
    return render(request,"contact.html",context)

#------------------------------------------------------------
def NewsletterView(request):
    msg=""
    if request.method=='POST':
        email=request.POST.get('newsltr')
        en1=newsletterModel(newsEmail=email)
        try:
            en1.save()
            msg='Your email address has been added on our newsletter list.'
        except Exception as e:
            msg= 'Error:'+str(e)
        cat_menu=Category.objects.all() 
        posts=Post.objects.all().order_by('-id')[:2]
        context={
            'cat_menu':cat_menu,
            'msg':msg,
            'posts':posts
        }       
    return render(request,"newsletter.html",context)



#-------------------------------------------------------------
def EmailSuccessView(request):
    msg=""
    if request.method=='POST':
        cname=request.POST.get('name')
        cemail=request.POST.get('email')
        cmesg=request.POST.get('message')
        mod=Contact(name=cname,email=cemail,mesg=cmesg)
        
        try:
            mod.save()
            msg='Your email has been sent.'
        except Exception as e:
            msg= 'Error:'+str(e)
    
    cat_menu=Category.objects.all()
    posts=Post.objects.all().order_by('-id')[:2]
    
    context={
        'cat_menu':cat_menu,
        'posts':posts,
        'msg':msg
    }
    return render(request,"emailsuccess.html",context)


#------------------------------------------------------------------
def AddCommentView(request, pk):

    msg=""
    cat_menu=Category.objects.all()
    if request.method=='POST':
        cname=request.POST.get('name','')
        print(cname)
        cbody=request.POST.get('body')
        cpost = get_object_or_404(Post,pk=pk)  # Get the post by primary key or return a 404 response if not found
        comment = Comment(name=cname,body=cbody,post=cpost)
        try:
            comment.save()
        except Exception as e:
            msg= 'Error:'+str(e)
        posts=Post.objects.all().order_by('-id')[:2]
        liked=False
        total_likes=cpost.total_likes()#total_likes is a function         
        if cpost.likes.filter(id=request.user.id).exists():
            liked=True
        #sorted in  descending order
        sorted_comments = cpost.comments.all().order_by('-date_added')

    context={
        'total_likes':total_likes,
        'liked':liked,
        'cat_menu':cat_menu,
        'sorted_comments':sorted_comments,
        'msg':msg,
        'post':cpost,
        'posts':posts,
        'html_content':cpost.recipe
    }
    return render(request, 'article_details.html', context)
    
