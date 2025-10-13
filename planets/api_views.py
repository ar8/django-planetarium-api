from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
# filtering and searching
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
# pagination
from rest_framework.pagination import PageNumberPagination
# models and serializers
from .models import Planet
from .serializers import PlanetSerializer, CustomTokenObtainPairSerializer
from .mixins import OptionalAuthMixin
from rest_framework_simplejwt.views import TokenObtainPairView
# cache
from django.core.cache import cache


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class PlanetPagination(PageNumberPagination):
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


class PlanetViewSet(OptionalAuthMixin, ModelViewSet):
    """
    Handles list, retrieve, create, update, and delete for planets.

    Get all planets, filter, search, order, paginate
    GET: /api/v1/planets/ =>  List all planets
    GET: /api/v1/planets/<name>/ => Retrieve a single planet by name.
    Filtering, searching, ordering, and pagination are supported, Examples:
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
    lookup_field = 'name'
    pagination_class = PlanetPagination

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
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
    ordering = ('id',)

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise Http404(f"Planet '{self.kwargs['name']}' not found")

    """
    Create a new planet
    POST:   /api/v1/planets/
    """
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
            status=status.HTTP_201_CREATED
        )

    """
    Update an existing planet
    PUT:    /api/v1/planets/<name>/	    full update.
    PATCH:	/api/v1/planets/<name>/	    Partial update.
    """
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache_key = f'planet_data_{instance.name}'
        cache.set(cache_key, serializer.data, timeout=60 * 15)
        return Response(serializer.data)

    """
    Delete a planet by name
    DELETE: /api/v1/planets/<name>/
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        cache.delete(f'planet_data_{instance.name}')
        instance.delete()
        return Response(
            {"message": f"Planet '{instance.name}' was deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
