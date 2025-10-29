from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from News.views import NewsViewSet, CategoryViewSet, ImageViewSet,CommentView,AdvertisementviewSet

router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'advertisements',AdvertisementviewSet, basename='advertisements')

news_router = NestedSimpleRouter(router, r'news', lookup='news')
news_router.register(r'image', ImageViewSet, basename='news-image')
news_router.register(r'comments',CommentView, basename='news-comments')
urlpatterns = [
    path('', include(router.urls)),
    path('', include(news_router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
