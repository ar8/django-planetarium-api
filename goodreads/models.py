from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        db_table = 'books'


class GoodreadsAccount(models.Model):
    """
    Model representing a user's Goodreads account.
    Missing table created after check Documentation as recommended:
    https://docs.djangoproject.com/en/5.2/ref/models/fields/#django.db.models.ManyToManyField
    https://docs.djangoproject.com/en/5.2/topics/db/queries/

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='goodreads_account', primary_key=True)
    friends = models.ManyToManyField('self', through='Friend', symmetrical=True, blank=True)
    user_books = models.ManyToManyField(Book, through='UserBook', related_name='user_owned_books', blank=True)

    class Meta:
        db_table = 'goodreads_accounts'


class UserBook(models.Model):
    id = models.BigAutoField(primary_key=True)
    goodreads_account = models.ForeignKey(GoodreadsAccount, on_delete=models.CASCADE, related_name='goodreads_account_user_books',)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_users',)

    class Meta:
        unique_together = ('goodreads_account', 'book')
        ordering = ['goodreads_account', 'book']
        verbose_name = 'UserBook'
        verbose_name_plural = 'UserBooks'
        db_table = 'user_books'


class Friend(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(GoodreadsAccount, on_delete=models.CASCADE, related_name='friendship_from')
    friend = models.ForeignKey(GoodreadsAccount, on_delete=models.CASCADE, related_name='friendship_to')

    class Meta:
        ordering = ['user']
        verbose_name = 'Friend'
        verbose_name_plural = 'Friends'
        db_table = 'friends_relationships'