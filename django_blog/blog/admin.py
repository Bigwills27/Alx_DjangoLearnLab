from django.contrib import admin
from .models import Post, Comment, Category, Like, PostView


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "published_date", "is_featured", "view_count")
    list_filter = ("published_date", "author", "category", "is_featured")
    search_fields = ("title", "content", "author__username")
    date_hierarchy = "published_date"
    list_editable = ("is_featured",)
    readonly_fields = ("view_count",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at")
    list_filter = ("created_at", "author")
    search_fields = ("content", "author__username", "post__title")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "post__title")


@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "ip_address", "timestamp")
    list_filter = ("timestamp",)
    search_fields = ("post__title", "user__username", "ip_address")
