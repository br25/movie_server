from rest_framework import serializers
from .models import FileData, Comments, Ratings, Notification


class FileDataSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = FileData
        fields = ['id', 'file_name', 'file_url', 'image_url', 'category', 'year', 'average_rating']

    def get_average_rating(self, obj):
        average_rating = obj.get_average_rating()
        return average_rating

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    file_data = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'user', 'file_data', 'comment', 'is_approved']


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Ratings
        fields = ['id', 'file_data', 'user', 'rating', 'average_rating']



class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'user', 'file_data', 'comment', 'is_approved']

    def get_user(self, obj):
        return self.context['request'].user.id

    def update(self, instance, validated_data):
        files_id = self.context['request'].data.get('file_data')
        files_instance = FileData.objects.get(id=files_id)
        instance.files = files_instance
        instance.is_approved = validated_data.get('is_approved', instance.is_approved)
        instance.save()
        return instance