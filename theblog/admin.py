from django.contrib import admin
from .models import Post,Category,Profile,Comment,Contact,newsletterModel

#When we want to display selected fields
class categoryAdmin(admin.ModelAdmin):
   list_display=('name','ct_slug')

class postAdmin(admin.ModelAdmin):
   list_display=('title','author','ingredients','recipe','post_date','category','category_slug','image','featured')

admin.site.register(Category,categoryAdmin)
admin.site.register(Post,postAdmin)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(newsletterModel)
admin.site.register(Contact)

