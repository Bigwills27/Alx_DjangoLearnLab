from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'actor', 'verb', 'target', 'timestamp', 'read')
    list_filter = ('read', 'timestamp', 'verb')
    search_fields = ('recipient__username', 'actor__username', 'verb')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(read=True)
        self.message_user(request, f'{queryset.count()} notifications marked as read.')
    mark_as_read.short_description = 'Mark selected notifications as read'
    
    def mark_as_unread(self, request, queryset):
        queryset.update(read=False)
        self.message_user(request, f'{queryset.count()} notifications marked as unread.')
    mark_as_unread.short_description = 'Mark selected notifications as unread'
