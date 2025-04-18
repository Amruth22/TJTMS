from django.contrib import admin
from .models import Task, TaskHistory, Comment, Attachment, Notification

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "assigned_to", "priority", "status", "deadline")
    list_filter = ("status", "priority", "assigned_to")
    search_fields = ("title", "description")

@admin.register(TaskHistory)
class TaskHistoryAdmin(admin.ModelAdmin):
    list_display = ("task", "assigned_to", "status", "timestamp")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("task", "user", "created_at")
    search_fields = ("comment",)

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("task", "uploaded_by", "created_at")

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "task", "type", "sent_at", "is_read")