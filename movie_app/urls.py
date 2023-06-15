from django.urls import path
from .views import (
    FileDataListAPIView,
    FileDataDetailAPIView,
    CommentListAPIView,
    CommentCreateAPIView,
    CommentDetailAPIView,
    ReviewListAPIView,
    ReviewDetailAPIView,
    SeenNotificationListView,
    NotificationUpdateAPIView,
)

urlpatterns = [
    path('', FileDataListAPIView.as_view(), name='filedata-list'),
    path('<int:pk>/', FileDataDetailAPIView.as_view(), name='filedata-detail'),
    path('comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('comments/create/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
    path('reviews/', ReviewListAPIView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetailAPIView.as_view(), name='review-detail'),
    path('notifications/', SeenNotificationListView.as_view(), name='seen-notifications'),
    path('notifications/<int:pk>/', NotificationUpdateAPIView.as_view(), name='notification-update'),
]
