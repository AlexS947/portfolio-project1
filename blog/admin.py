from django.contrib import admin
from .models import News, Category, Comment, Vote, Topic

class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'author', 'created_at')

admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(News)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'text', 'is_approved')
    list_filter = ('is_approved',)
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

admin.site.unregister(Comment)
admin.site.register(Comment, CommentAdmin)
