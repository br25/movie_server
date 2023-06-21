from django.contrib import admin
from .models import FileData, Comments, Notification, Ratings

admin.site.register(FileData)
admin.site.register(Comments)
admin.site.register(Notification)
admin.site.register(Ratings)
