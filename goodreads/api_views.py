from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

# filtering and searching
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
# pagination
from rest_framework.pagination import PageNumberPagination

# models and serializers
from .models import GoodreadsAccount
from .serializers import GoodreadsAccountSerializer 
from .mixins import OptionalAuthMixin
from .serializers import BookSerializer
from rest_framework.decorators import action
# path action
from rest_framework.decorators import action


class GoodreadsViewSet(OptionalAuthMixin, ModelViewSet):
    """
    Handles list, retrieve, create, update, and delete for Goodreads accounts.
    GET: /api/v1/goodreads/ =>  List all goodreads accounts
    GET: /api/v1/goodreads/{id}/ => Retrieve a specific goodreads account by ID
    GET: /api/v1/goodreads/{user_username}/network_books/ => Get friends' books for a given user ID
    """
    queryset = GoodreadsAccount.objects.all()
    serializer_class = GoodreadsAccountSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user__username']
    search_fields = ['user__username', 'book__name']
    ordering_fields = ['user__username']
    ordering = ['user__username']
    lookup_field = 'user__username'  # assuming user is identified by username

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    @action(detail=False, methods=['get'], url_path=r'(?P<user_username>[^/.]+)/network_books')
    def get_network_books(self, request, user_username=None):

        # Get the account
        goodreads_account = GoodreadsAccount.objects.get(user__username=user_username)

        # Get friends' books
        friends = goodreads_account.friends.all()
        friends_books = set()
        for friend in friends:
            friends_books.update(friend.user_books.all())

        friends_books_list = list(friends_books)
        serializer = BookSerializer(friends_books_list, many=True)

        # Get user's books
        user_books = goodreads_account.user_books.all()
        user_serializer = BookSerializer(user_books, many=True)

        data = {
            'user': user_username,
            'user_books': user_serializer.data,
            'friends_books': serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)