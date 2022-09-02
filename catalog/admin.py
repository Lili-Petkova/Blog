from django.contrib import admin

from .models import Comment, Post


class CommentInlineModelAdmin(admin.TabularInline):
    model = Comment


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'short_text', 'full_text', 'author', 'status']
    fields = ['title', 'short_text', 'full_text', 'image', 'author', 'pub_date']
    raw_id_fields = ['author', ]
    date_hierarchy = "pub_date"
    search_fields = ["author", "title"]
    actions = ["change_status_to_deferred", "change_status_to_published"]
    inlines = [CommentInlineModelAdmin]

    def change_status_to_deferred(self, request, queryset):
        queryset.update(status='deferred')
    change_status_to_deferred.short_description = "Status: deferred"

    def change_status_to_published(self, request, queryset):
        queryset.update(status='published')
    change_status_to_published.short_description = "Status: published"


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ["author", "text", "post", "status"]
    fields = ['author', 'text', "post", "pub_date"]
    search_fields = ["post"]
    date_hierarchy = "pub_date"
    actions = ["allow_comment", "block_comment"]

    def allow_comment(self, request, queryset):
        queryset.update(status=True)

    allow_comment.short_description = "Allow comment to publication"

    def block_comment(self, request, queryset):
        queryset.update(status=False)

    block_comment.short_description = "Block comment to publication"
