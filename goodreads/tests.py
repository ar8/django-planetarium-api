from django.test import TestCase


class GoodreadsAPITestCase(TestCase):
    def setUp(self):
        # Set up initial data for testing
        from django.contrib.auth.models import User
        from .models import GoodreadsAccount, Book, UserBook, Friend

        self.user1 = User.objects.create_user(username='test_1', password='password123')
        self.user2 = User.objects.create_user(username='test_2', password='password123')

        self.account1 = GoodreadsAccount.objects.create(user=self.user1)
        self.account2 = GoodreadsAccount.objects.create(user=self.user2)

        self.book1 = Book.objects.create(name="1984", author="George Orwell")
        self.book2 = Book.objects.create(name="Brave New World", author="Aldous Huxley")

        UserBook.objects.create(goodreads_account=self.account1, book=self.book1)
        UserBook.objects.create(goodreads_account=self.account2, book=self.book2)

        Friend.objects.create(user=self.account1, friend=self.account2)

    def test_goodreads_endpoint(self):
        # Example test for Goodreads endpoint
        response = self.client.get('/api/v1/goodreads/test_1/network_books/')
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed
