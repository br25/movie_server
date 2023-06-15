from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import FileData, Comment, Review, Notification
from .serializers import FileDataSerializer, CommentSerializer, ReviewSerializer, NotificationSerializer, NotificationUpdateSerializer

from rest_framework.response import Response


class FileDataListAPIView(generics.ListCreateAPIView):
    queryset = FileData.objects.all()
    serializer_class = FileDataSerializer
    # permission_classes = (IsAdminUser,)


class FileDataDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FileData.objects.all()
    serializer_class = FileDataSerializer


class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(is_approved=True)

class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SeenNotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    # permission_classes = (IsAdminUser,)

class NotificationUpdateAPIView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationUpdateSerializer


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ReviewListAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
