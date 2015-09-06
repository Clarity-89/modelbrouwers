from rest_framework import serializers

from brouwers.forum_tools.api.serializers import TopicSerializer
from brouwers.users.api.serializers import UserSerializer
from brouwers.utils.api.fields import ThumbnailField
from ..models import Album, Photo
from ..serializers import PreferencesSerializer  # pragma: no cover


class AlbumSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    topic = TopicSerializer()

    class Meta:
        model = Album
        fields = ('id', 'user', 'title', 'description', 'public', 'topic')


class UploadPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('album', 'image', 'description')


class PhotoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    image = ThumbnailField(
        (('large', '1280'), ('thumb', '300x225')),  # large photo + actual thumb
        opts={'crop': 'center', 'upscale': False}
    )

    class Meta:
        model = Photo
        fields = ('id', 'user', 'description', 'image', 'width', 'height', 'uploaded', 'order')


class ForumPhotoSerializer(serializers.ModelSerializer):
    user = UserSerializer
    image = ThumbnailField(
        (('large', '1024x1024'), ('thumb', '300x225')),
        opts={'crop': False, 'upscale': False}
    )

    class Meta:
        model = Photo
        fields = ('id', 'user', 'description', 'image')