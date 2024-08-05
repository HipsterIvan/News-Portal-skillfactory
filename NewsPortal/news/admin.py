from django.contrib import admin
from .models import Post, Author, Category, PostCategory, Comment #SubscribersCategory


class CategoryInLine(admin.TabularInline):
    model = PostCategory
    extra = 1
    
class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = (CategoryInLine, )

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Comment)
#admin.site.register(SubscribersCategory)