# API endpoints for Planet app
from django.urls import path
from planets.views import PlanetServiceView
from planets.api_views import PlanetListAPIView, PlanetDetailAPIView, PlanetCreateAPIView, PlanetUpdateAPIView, PlanetDeleteAPIView

app_name = 'planets'

urlpatterns = [
    path('service/', PlanetServiceView.as_view(), name='planet-service'),

    # Planet API with clear structure
    path('', PlanetListAPIView.as_view(http_method_names=['get']), name='listing'),
    path('create/', PlanetCreateAPIView.as_view(http_method_names=['post']), name="create"),
    path('<str:name>/', PlanetDetailAPIView.as_view(http_method_names=['get']), name='detail'),
    path('<str:name>/update/', PlanetUpdateAPIView.as_view(http_method_names=['put']), name="update"),
    path('<str:name>/delete/', PlanetDeleteAPIView.as_view(http_method_names=['delete']), name="delete"),
]
