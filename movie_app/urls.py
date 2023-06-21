from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    FileDataList,
    FileDataDetails,
    CommentList,
    CommentCreate,
    RatingCreate,
    NotificationList,
    NotificationUpdate,
)

urlpatterns = [
    path('filedata/', FileDataList.as_view(), name='filedata-list'),
    path('filedata/<int:pk>/', FileDataDetails.as_view(), name='filedata-details'),
    path('comments/', CommentList.as_view(), name='comment-list'),
    path('comment/create/<int:file_id>/', CommentCreate.as_view(), name='comment-create'),
    path('rating/create/<int:file_id>/', RatingCreate.as_view(), name='rating-create'),
    path('notifications/', NotificationList.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', NotificationUpdate.as_view(), name='notification-update'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)