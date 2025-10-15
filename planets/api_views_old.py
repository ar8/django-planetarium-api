from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from .models import Planet
from .serializers import PlanetSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
# pagination
from rest_framework.pagination import PageNumberPagination
# token authentication and security
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# for testing to avoid authentication
from .mixins import OptionalAuthMixin
# cache
from django.core.cache import cache


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    helper functions to get Bearer token to test security of the API
    Example: http://localhost:8000/auth/token/
    """
    serializer_class = CustomTokenObtainPairSerializer


class PlanetPagination(PageNumberPagination):
    """
    example:
    api/v1/planets/?page=2 => get page 2
    api/v1/planets/?page=3&page_size=5 => page 3, with 5 results per page
    api/v1/planets/?limit=5&offset=10 => skip 10, return 5
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })


class PlanetListAPIView(OptionalAuthMixin, ListAPIView):
    """
    Get all planets, filter, search, order, paginate
    example:
    api/v1/planets/
    api/v1/planets/?name=Earth
    api/v1/planets/?climates=temperate
    api/v1/planets/?terrains=forest
    api/v1/planets/?population=100
    api/v1/planets/?search=Earth
    api/v1/planets/?ordering=name
    api/v1/planets/?ordering=-population
    api/v1/planets/?page=2
    api/v1/planets/?page=3&page_size=5
    api/v1/planets/?limit=5&offset=10
    api/v1/planets/?climates__name=Arid
    api/v1/planets/?terrains__name=Rocky
    api/v1/planets/?population__gte=10&population__lte=500
    """
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    pagination_class = PlanetPagination
    filterset_fields = {
        'name': ['icontains', 'exact'],
        'population': ['exact', 'gte', 'lte'],
        'created_at': ['exact', 'gte', 'lte'],
        'updated_at': ['exact', 'gte', 'lte'],
        'climates__name': ['exact', 'icontains'],
        'terrains__name': ['exact', 'icontains'],

    }
    search_fields = ('name', 'climates__name', 'terrains__name', 'population', 'created_at', 'updated_at')
    ordering_fields = ('name', 'created_at', 'updated_at')
    ordering = ('id',)  # default ordering

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class PlanetDetailAPIView(OptionalAuthMixin, RetrieveAPIView):
    """
    Get a planet by name
    example:
    api/v1/planets/name/Earth/
    api/v1/planets/name/Mars/
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
