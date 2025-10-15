from django.contrib import admin
from . import models


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')
    search_fields = ('name', 'author')
    ordering = ('name',)


@admin.register(models.GoodreadsAccount)
class GoodreadsAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_friends', 'get_user_books')
    search_fields = ('user__username', 'user__email', 'user_books__name', 'friends__user__username')

    def get_friends(self, obj):
        return ", ".join([friend.user.username for friend in obj.friends.all()])
    get_friends.short_description = 'Friends'

    def get_user_books(self, obj):
        return ", ".join([book.name for book in obj.user_books.all()])
    get_user_books.short_description = 'User Books'
    ordering = ('user__username',)


@admin.register(models.UserBook)
class UserBookAdmin(admin.ModelAdmin):
    list_display = ('id', 'goodreads_account', 'book')
    search_fields = ('goodreads_account__user__username', 'book__name')
    ordering = ('goodreads_account__user__username', 'book__name')
    readonly_fields = ('id',)


@admin.register(models.Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'friend')
    search_fields = ('user__user__username', 'friend__user__username')
    ordering = ('user__user__username', 'friend__user__username')
    readonly_fields = ('id',)