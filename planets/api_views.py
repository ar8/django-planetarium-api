from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from .models import Planet
from .serializers import PlanetSerializer
from django.http import Http404
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

# pagination
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

# token authentication and security
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# for testing to avoid authentication
from .mixins import OptionalAuthMixin
from django.conf import settings
from rest_framework.permissions import IsAuthenticated, AllowAny

# cache
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    helper functions to get Bearer token to test security of the API
    Example: http://localhost:8000/auth/token/
    """
    serializer_class = CustomTokenObtainPairSerializer


# -----------------------------
# Planet API
# -----------------------------
class PlanetPagination(LimitOffsetPagination, PageNumberPagination):
    """
    example:
    planets/?page=2 => get page 2
    planets/?page=3&page_size=5 => page 3, with 5 results per page
    planets/?limit=5&offset=10 => skip 10, return 5
    """
    default_limit = 10
    page_size_query_param = 'page_size'
    max_limit = 100
    page_size = 10
    page_query_param = 'page'
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_page_size = 100


class PlanetListAPIView(OptionalAuthMixin, ListAPIView):
    """
    Get all planets, filter, search, order, paginate
    example:
    planets/
    planets/?name=Earth
    planets/?climates=temperate
    planets/?terrains=forest
    planets/?population=1000
    planets/?search=Earth
    planets/?ordering=name
    planets/?ordering=-population
    planets/?page=2
    planets/?page=3&page_size=5
    planets/?limit=5&offset=10
    planets/?climates__name=temperate
    planets/?terrains__name=forest
    planets/?population__gte=1000&population__lte=5000
    """
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    pagination_class = PlanetPagination
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'climates__name': ['exact', 'icontains'],
        'terrains__name': ['exact', 'icontains'],
        'population': ['exact', 'gte', 'lte'],
        'created_at': ['exact', 'gte', 'lte'],
        'updated_at': ['exact', 'gte', 'lte'],
    }
    search_fields = ('name', 'climates__name', 'terrains__name', 'population', 'created_at', 'updated_at')
    ordering_fields = ('name', 'created_at', 'updated_at')
    ordering = ('name',)  # default ordering

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class PlanetDetailAPIView(OptionalAuthMixin, RetrieveAPIView):
    """
    Get a planet by name
    example:
    planets/name/Earth/
    planets/name/Mars/
    """
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    # lookup by name instead of id
    lookup_field = 'name'

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise Http404(f"Planet '{self.kwargs['name']}' not found")


class PlanetCreateAPIView(OptionalAuthMixin, CreateAPIView):
    """
    Create a new planet
    /api/v1/planets/create/
    """
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        planet_name = serializer.validated_data.get('name')
        if Planet.objects.filter(name=planet_name).exists():
            raise Http404(f"Planet '{planet_name}' already exists.")
        serializer.save()
        # update cache
        cache_key = f'planet_data_{planet_name}'
        cache.set(cache_key, serializer.data, timeout=60 * 15)

        return Response(
            {"message": f"Planet '{planet_name}' was created successfully.", "planet": serializer.data},
            status=status.HTTP_201_CREATED)


class PlanetUpdateAPIView(OptionalAuthMixin, RetrieveUpdateAPIView):
    """
    Update a planet by name
    /api/v1/planets/update/Earth/
    /api/v1/planets/update/Mars/
    """
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    lookup_field = 'name'

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise Http404(f"Planet '{self.kwargs['name']}' not found")

    def perform_update(self, serializer):
        planet = self.get_object()
        serializer.save()
        cache_key = f'planet_data_{planet.name}'
        cache.set(cache_key, serializer.data, timeout=60 * 15)


class PlanetDeleteAPIView(OptionalAuthMixin, DestroyAPIView):
    """
    Delete a planet by name
    /api/v1/planets/delete/Earth/
    /api/v1/planets/delete/Mars/
    """
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    lookup_field = 'name'

    def get_object(self):
        """Return planet or raise custom 404 message"""
        try:
            return super().get_object()
        except Http404:
            raise Http404(f"Planet '{self.kwargs['name']}' not found")

    def perform_destroy(self, instance):
        cache.delete(f'planet_data_{instance.name}')
        instance.delete()
