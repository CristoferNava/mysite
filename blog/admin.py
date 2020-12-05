from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)} # autofill the slug using the title
    raw_id_fields = ('author',)
    # displays a lookup widget for searching the author
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
