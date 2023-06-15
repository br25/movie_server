from django.contrib import admin
from .models import FileData, Comment, Notification, Review

admin.site.register(FileData)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Review)
