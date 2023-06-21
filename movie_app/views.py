from rest_framework import generics, status
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.db.models import Avg
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from .models import FileData, Comments, Ratings, Notification
from .serializers import (
    FileDataSerializer,
    CommentSerializer,
    RatingSerializer,
    NotificationSerializer,
)


class FileDataList(generics.ListAPIView):
    queryset = FileData.objects.order_by('id')
    serializer_class = FileDataSerializer

    # Data Searching
    def get_queryset(self):
        queryset = super().get_queryset()
        file_name = self.request.query_params.get('file_name')
        category = self.request.query_params.get('category')
        year = self.request.query_params.get('year')

        if file_name:
            queryset = queryset.filter(file_name__icontains=file_name)
        if category:
            queryset = queryset.filter(category__icontains=category)
        if year:
            queryset = queryset.filter(year__icontains=year)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        paginator = Paginator(queryset, 20)  # 20 items per page
        page = request.GET.get('page')
        paginated_queryset = paginator.get_page(page)

        serializer = self.serializer_class(paginated_queryset, many=True)
        serialized_data = serializer.data

        return render(request, 'filedata.html', {
            'data_list': serialized_data,
            'paginator': {
                'page': paginated_queryset.number,
                'pages': paginator.num_pages,
                'total': paginator.count,
            }
        })


class FileDataDetails(generics.RetrieveAPIView):
    queryset = FileData.objects.all()
    serializer_class = FileDataSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serialized_data = serializer.data

        # Retrieve the comments related to the file data instance
        comments = Comments.objects.filter(file_data=instance)  # Fix the model name here
        comment_serializer = CommentSerializer(comments, many=True)
        comment_data = comment_serializer.data

        return render(request, 'filedata_details.html', {'data_details': serialized_data, 'comments': comment_data})


class CommentList(generics.ListAPIView):
    serializer_class = CommentSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'filedata_details.html'

    def get_queryset(self):
        return Comments.objects.filter(is_approved=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        comments_data = serializer.data
        return Response({'comments': comments_data})

class CommentCreate(generics.CreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

    def get(self, request, *args, **kwargs):
        return render(request, 'comment_create.html')

    def post(self, request, *args, **kwargs):
        file_id = kwargs.get('file_id')
        mutable_data = request.data.copy()
        mutable_data['file_data'] = file_id
        mutable_data['user'] = request.user.id  # Set the user_id field to the ID of the logged-in user
        return self.create(request, data=mutable_data, *args, **kwargs)

    def perform_create(self, serializer):
        file_id = self.kwargs.get('file_id')
        file_data = get_object_or_404(FileData, pk=file_id)
        serializer.save(file_data=file_data, user=self.request.user)

class RatingCreate(generics.CreateAPIView):
    queryset = Ratings.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        file_data_id = kwargs.get('file_id')  # Assuming 'file_id' is passed as a URL parameter
        ratings = Ratings.objects.filter(file_data=file_data_id)
        context = {'ratings': ratings, 'file_id': file_data_id}
        return render(request, 'rating_create.html', context)

    def post(self, request, *args, **kwargs):
        file_data_id = kwargs.get('file_id')
        mutable_data = request.data.copy()  # Create a mutable copy of the data
        mutable_data['file_data'] = file_data_id  # Modify the mutable data
        return self.create(request, data=mutable_data, *args, **kwargs)  # Pass the modified data to create method


class NotificationList(generics.ListAPIView):
    queryset = Notification.objects.filter(is_approved=False)
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser, ]


class NotificationUpdate(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdminUser, ]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_approved = bool(request.data.get('is_approved'))
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)