from rest_framework.viewsets import ModelViewSet
from .models import News, Category, Comment, Advertisement, ImageModel
from .serializers import NewsSerializer, CategorySerializer, ImageSerializer,CommentSerializer,AdvertisementSerializer
from rest_framework import filters
from News.paginations import DefaultPagination
from api.permissons import IsStaffOrReadOnly
from News.permissions import IsReviewAuthorOrReadonly
from rest_framework.permissions import IsAdminUser
class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'category__name']
    pagination_class = DefaultPagination
    permission_classes = [IsStaffOrReadOnly]


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsStaffOrReadOnly]


class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        # Swagger schema generate করার সময় error এড়ানোর জন্য check
        if getattr(self, 'swagger_fake_view', False):
            return ImageModel.objects.none()

        news_pk = self.kwargs.get('news_pk')
        return ImageModel.objects.filter(news_id=news_pk)

    def perform_create(self, serializer):
        news_pk = self.kwargs.get('news_pk')
        serializer.save(news_id=news_pk)

class CommentView(ModelViewSet):
    serializer_class=CommentSerializer
    permission_classes = [IsReviewAuthorOrReadonly]

    def get_queryset(self):
        news_pk = self.kwargs.get('news_pk')
        return Comment.objects.filter(news_id=news_pk)
    def perform_create(self, serializer):
        news_id=self.kwargs['news_pk']
        serializer.save(user=self.request.user,news_id=news_id)

class AdvertisementviewSet(ModelViewSet):
    queryset=Advertisement.objects.all()
    serializer_class=AdvertisementSerializer
    permission_classes=[IsStaffOrReadOnly]