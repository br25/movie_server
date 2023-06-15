from rest_framework import serializers
from .models import FileData, Comment, Review, Notification
from movie_auth.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_approved = serializers.BooleanField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'files', 'comment', 'is_approved']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'files', 'user', 'rating']

    def create(self, validated_data):
        user = self.context['request'].user

        validated_data['user'] = user

        return super().create(validated_data)


class FileDataSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = FileData
        fields = ['id', 'file_name', 'file_url', 'image_url', 'average_rating']

    def get_average_rating(self, obj):
        reviews = Review.objects.filter(files=obj)
        if reviews:
            total_ratings = sum([review.rating for review in reviews])
            average_rating = total_ratings / len(reviews)
            return average_rating
        else:
            return 0


class NotificationSerializer(serializers.ModelSerializer):
    is_approve = serializers.SerializerMethodField()
    comment = CommentSerializer()

    def get_is_approve(self, obj):
        comment = obj.comment
        if comment and hasattr(comment, 'is_approved'):
            return comment.is_approved
        return None

    class Meta:
        model = Notification
        fields = ['id', 'user', 'comment', 'message', 'timestamp', 'is_seen', 'is_approve']


class NotificationUpdateSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(read_only=True)
    files = serializers.ReadOnlyField(source='comment.files.name')
    is_approved = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'user', 'comment', 'message', 'timestamp', 'is_seen', 'is_approve', 'files', 'is_approved']
        read_only_fields = ['id', 'user', 'comment', 'message', 'timestamp', 'files']

    def get_is_approved(self, instance):
        return instance.comment.is_approved

    def update(self, instance, validated_data):
        instance.is_seen = validated_data.get('is_seen', instance.is_seen)
        instance.is_approve = validated_data.get('is_approve', instance.is_approve)
        instance.save()

        comment = instance.comment
        if comment:
            comment.is_approved = instance.is_approve
            comment.save()

        return instance