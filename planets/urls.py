# API endpoints for Planet app
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from planets.api_views import PlanetViewSet


router = DefaultRouter()
router.register(r'planets', PlanetViewSet, basename='planet')

urlpatterns = router.urls

urlpatterns = [
    # include all ViewSet routes CRUD operations
    path('', include(router.urls)),
]
