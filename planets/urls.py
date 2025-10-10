from django.urls import path
from planets.api_views import PlanetListAPIView, PlanetDetailAPIView, CustomTokenObtainPairView, PlanetCreateAPIView, PlanetUpdateAPIView, PlanetDeleteAPIView
from planets.views import PlanetServiceView

urlpatterns = [
    path('api/v1/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/planets/service/', PlanetServiceView.as_view(), name='planet-service'),
    # -----------------------------
    # Planet API
    # -----------------------------
    path('api/v1/planets/', PlanetListAPIView.as_view(), name='planet-listing'),
    path('api/v1/planets/<str:name>/', PlanetDetailAPIView.as_view(), name='planet-detail'),
    path("api/v1/planets/create/", PlanetCreateAPIView.as_view(), name="planet-create"),
    path("api/v1/planets/update/<str:name>/", PlanetUpdateAPIView.as_view(), name="planet-update"),
    path("api/v1/planets/delete/<str:name>/", PlanetDeleteAPIView.as_view(), name="planet-delete"),
]