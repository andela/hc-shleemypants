from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','status','created') #the fields we want displayed on the admin site
    list_filter = ('status','created','publish','author') #the filters we want the admin to use on the right bar
    search_fields = ('title','author') #search fields we want to search all the posts with
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

admin.site.register(Post, PostAdmin)