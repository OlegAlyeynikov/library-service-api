import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from book.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="borrowings")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="borrowings"
    )

    @staticmethod
    def validate_book_inventory(inventory: int, title: str, error_to_raise) -> None:
        if not (inventory > 0):
            raise error_to_raise(
                {
                    "book": f"There is currently no book for borrowing with title: {title}"
                }
            )

    @staticmethod
    def validate_correct_date(
        borrow_date: datetime.date, expected_date: datetime.date, error_to_raise
    ) -> None:
        if borrow_date < datetime.date.today():
            raise error_to_raise(
                {
                    "not possible date": "Borrow date must be more or equal than date today."
                }
            )
        if expected_date <= borrow_date:
            raise error_to_raise(
                {"not possible date": "Expected date must be more than borrow date."}
            )

    def clean(self):
        Borrowing.validate_book_inventory(
            self.book.inventory, self.book.title, ValidationError
        )
        Borrowing.validate_correct_date(
            self.borrow_date, self.expected_return_date, ValidationError
        )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.actual_return_date:
            self.full_clean()
            return super(Borrowing, self).save(
                force_insert, force_update, using, update_fields
            )
        return super(Borrowing, self).save(
            force_insert, force_update, using, update_fields
        )

    class Meta:
        ordering = ["borrow_date"]

    def __str__(self):
        return f"{self.borrow_date}"
