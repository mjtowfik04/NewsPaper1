from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import News, Category, Comment, Advertisement, ImageModel
from .serializers import (
    NewsSerializer,
    CategorySerializer,
    ImageSerializer,
    CommentSerializer,
    AdvertisementSerializer,
)
from News.paginations import DefaultPagination
from api.permissions import IsStaffOrReadOnly
from News.permissions import IsReviewAuthorOrReadonly



# NEWS VIEWSET (CATEGORY FILTER FIXED)
class NewsViewSet(ModelViewSet):
    serializer_class = NewsSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "category__name"]

    def get_queryset(self):
        queryset = News.objects.all()
        category = self.request.query_params.get("category")

        if category:
            queryset = queryset.filter(category_id=category)

        return queryset



# CATEGORY VIEWSET
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]


# IMAGE VIEWSET
@method_decorator(csrf_exempt, name="dispatch")
class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [IsStaffOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return ImageModel.objects.none()

        news_pk = self.kwargs.get("news_pk")
        return ImageModel.objects.filter(news_id=news_pk)

    def perform_create(self, serializer):
        news_pk = self.kwargs.get("news_pk")
        serializer.save(news_id=news_pk)


# COMMENT VIEWSET
class CommentView(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsReviewAuthorOrReadonly]

    def get_queryset(self):
        news_pk = self.kwargs.get("news_pk")
        return Comment.objects.filter(news_id=news_pk)

    def perform_create(self, serializer):
        news_pk = self.kwargs.get("news_pk")
        serializer.save(user=self.request.user, news_id=news_pk)


# ADVERTISEMENT VIEWSET
class AdvertisementviewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsStaffOrReadOnly]