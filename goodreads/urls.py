# API endpoints for Planet app
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from goodreads.api_views import GoodreadsViewSet


router = DefaultRouter()
router.register(r'goodreads', GoodreadsViewSet, basename='goodreads')

urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
]
