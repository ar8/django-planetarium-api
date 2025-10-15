from rest_framework import serializers
from .models import Book, UserBook, Friend, GoodreadsAccount
from django.db import models


class UserBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBook
        read_only_fields = ['id']
        ordering = ['user', 'book']
        verbose_name = 'UserBook'
        verbose_name_plural = 'UserBooks'
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'author']
        read_only_fields = ['id']
        ordering = ['name']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        db_table = 'books'
        fields = '__all__'


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        read_only_fields = ['id']
        ordering = ['user']
        verbose_name = 'Friend'
        verbose_name_plural = 'Friends'
        fields = '__all__'


class GoodreadsAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodreadsAccount
        read_only_fields = ['id']
        ordering = ['user']
        verbose_name = 'GoodreadsAccount'
        verbose_name_plural = 'GoodreadsAccounts'
        fields = '__all__'
