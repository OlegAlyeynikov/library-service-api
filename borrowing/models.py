from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()  # Ожидаемая дата возвращения
    actual_return_date = models.DateField(null=True)  # Фактическая дата возвращения
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="Borrowing")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="Borrowing"
    )

    class Meta:
        ordering = ["borrow_date"]

    def __str__(self):
        return f"{self.borrow_date}"
