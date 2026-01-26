from rest_framework import serializers
from News.models import Category, News, ImageModel, Comment, Advertisement

class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = ImageModel
        fields = ['id', 'image']
        extra_kwargs = {'image': {'required': True}}

class NewsSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    image = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = [
            'id', 'title', 'content', 'category', 'url',
            'image', 'is_featured', 'is_published', 
            'created_at', 'updated_at', 'published_at'
        ]

    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(f"/api/news/{obj.pk}/")

class CategorySerializer(serializers.ModelSerializer):
    news = NewsSerializer(many=True, read_only=True)  # এই লাইনে category.news.all() থেকে সব news আসবে

    class Meta:
        model = Category
        fields = ['id', 'name','news']  # news add করা হয়েছে

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']
        read_only_fields = ['user', 'is_approved']

class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['id', 'content', 'image']