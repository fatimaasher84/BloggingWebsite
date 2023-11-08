from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

#for function based views
from .views import BlogView,HomeView,AboutView,NewsView,ContactView,CategoryView,NewsletterView,AddCommentView,CategoryListView,LikeView,footerView,EmailSuccessView

#class based views
from .views import ArticleDetailView,AddPostView,UpdatePostView,DeletePostView,AddCategoryView
urlpatterns = [

    #CLASS BASED URLS
    path('article/<int:pk>/',ArticleDetailView.as_view(),name="article-detail"), #int means an integer number and pk is primary key
    path('add_post/',AddPostView.as_view(),name="add_post"),
    path('add_category/',AddCategoryView.as_view(),name="add_category"),
    #path('blog/',BlogView.as_view(),name="blog"),
    #path('blog/<int:page>/',BlogView.as_view(),name="blog"),
    path('article/edit/<int:pk>/',UpdatePostView.as_view(),name="update_post"),
    path('article/<int:pk>/remove/',DeletePostView.as_view(),name="delete_post"),
    path('article/<int:pk>/comment/',AddCommentView,name="add_comment"),
    #path('tinymce/', include('tinymce.urls')),
    
    #function based urls
    path('',HomeView,name="home"),
    path('about/',AboutView,name="about"),
    path('news/',NewsView,name="news"),
    path('blog/',BlogView,name="blog"),
    path('newsletter/',NewsletterView,name="newsletter"),
    path('emailsuccess/',EmailSuccessView,name="emailsuccess"),
    path('contact/',ContactView,name="contact"),
    path('category/<slug>/',CategoryView,name="category"),
    path('category-list/',CategoryListView,name="category-list"),
    path('like/<int:pk>/',LikeView,name="like_post"),
    path('footer/',footerView,name="footer"),
]

