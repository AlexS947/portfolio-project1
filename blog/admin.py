from django.contrib import admin
from .models import News, Category, Comment, Vote, Topic

# Topic Admin
class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'created_at')

# Comment Admin
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'text', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

# Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Register models only once
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Vote)
admin.site.register(News)
admin.site.register(Category, CategoryAdmin)
