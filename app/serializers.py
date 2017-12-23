from rest_framework import serializers

from app.models import NewsModel


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsModel
        fields = ('id', 'title', 'image_url', 'use_in_report',
                  'comments', 'votes', 'category')