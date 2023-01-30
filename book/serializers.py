from rest_framework import serializers

from book.models import Book
from borrowing.models import Borrowing


def book_available():
    book = Book.objects.get(pk=id)
    borrowings = Borrowing.objects.filter(book=book)
    # book_inventory = len(borrowings)


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "authors", "cover", "inventory", "daily_fee")
