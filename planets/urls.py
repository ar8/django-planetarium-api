from django.urls import path
from planets.views import PlanetServiceView
from planets.api_views import PlanetListAPIView, PlanetDetailAPIView, PlanetCreateAPIView, PlanetUpdateAPIView, PlanetDeleteAPIView

app_name = 'planets'

urlpatterns = [
    path('service/', PlanetServiceView.as_view(), name='planet-service'),

    # Planet API with clear structure
    path('', PlanetListAPIView.as_view(), name='listing'),
    path('create/', PlanetCreateAPIView.as_view(), name="create"),
    path('detail/<str:name>/', PlanetDetailAPIView.as_view(), name='detail'),
    path('update/<str:name>/', PlanetUpdateAPIView.as_view(), name="update"),
    path('delete/<str:name>/', PlanetDeleteAPIView.as_view(), name="delete"),
]