from django.core.management.base import BaseCommand
from goodreads.models import Book, GoodreadsAccount, UserBook, Friend
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **options):
        # Flush database first
        self.flush_data()

        # Create users
        alice = User.objects.create_user(username='Alice', password='password123')
        bob = User.objects.create_user(username='Bob', password='password123')
        charlie = User.objects.create_user(username='Charlie', password='password123')
        david = User.objects.create_user(username='David', password='password123')
        lolo = User.objects.create_user(username='Lolo', password='password123')
        momo = User.objects.create_user(username='Momo', password='password123')  

        # create profiles
        alice_account = GoodreadsAccount.objects.create(user=alice)
        bob_account = GoodreadsAccount.objects.create(user=bob)
        charlie_account = GoodreadsAccount.objects.create(user=charlie)
        david_account = GoodreadsAccount.objects.create(user=david)
        lolo_account = GoodreadsAccount.objects.create(user=lolo)
        momo_account = GoodreadsAccount.objects.create(user=momo)

        # Create books
        naruto = Book.objects.create(name='Naruto', author='Masashi Kishimoto')
        fairy_tail = Book.objects.create(name='Fairy Tail', author='Hiro Mashima')
        one_piece = Book.objects.create(name='One Piece', author='Eiichiro Oda')
        attack_on_titan = Book.objects.create(name='Attack on Titan', author='Hajime Isayama')
        boku_no_hero_academia = Book.objects.create(name='Boku no Hero Academia', author='Kohei Horikoshi')
        black_clover = Book.objects.create(name='Black Clover', author='Yūki Tabata')
        secrets_of_the_silent_witch = Book.objects.create(name='Secrets of the Silent Witch', author='Anita Sahu')

        # Assign books to users
        UserBook.objects.bulk_create([
            # alice books
            UserBook(goodreads_account=alice_account, book=naruto),
            UserBook(goodreads_account=alice_account, book=fairy_tail),
            UserBook(goodreads_account=alice_account, book=one_piece),
            UserBook(goodreads_account=alice_account, book=attack_on_titan),
            # bob books
            UserBook(goodreads_account=bob_account, book=one_piece),
            UserBook(goodreads_account=bob_account, book=attack_on_titan),
            # charlie books
            UserBook(goodreads_account=charlie_account, book=boku_no_hero_academia),
            UserBook(goodreads_account=charlie_account, book=black_clover),
            # david books
            UserBook(goodreads_account=david_account, book=secrets_of_the_silent_witch),
            UserBook(goodreads_account=david_account, book=one_piece),
            # lolo books
            UserBook(goodreads_account=lolo_account, book=fairy_tail),
            UserBook(goodreads_account=lolo_account, book=attack_on_titan),
            # momo books
            UserBook(goodreads_account=momo_account, book=boku_no_hero_academia),
            UserBook(goodreads_account=momo_account, book=black_clover),
        ])
        # Assign friends to users
        Friend.objects.bulk_create([
            Friend(user=alice_account, friend=bob_account),
            Friend(user=alice_account, friend=charlie_account),
            Friend(user=alice_account, friend=david_account),
            Friend(user=alice_account, friend=lolo_account),
            Friend(user=bob_account, friend=david_account),
            Friend(user=bob_account, friend=lolo_account),
            Friend(user=charlie_account, friend=momo_account),
            Friend(user=charlie_account, friend=bob_account),
        ])

    def flush_data(self):
        Book.objects.all().delete()
        User.objects.all().delete()
        GoodreadsAccount.objects.all().delete()
        UserBook.objects.all().delete()
        Friend.objects.all().delete()