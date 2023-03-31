import datetime
from book.models import Book
from borrowing.models import Borrowing
from user.models import User


def get_books_with_overdue_borrow() -> str or list:
    overdue_borrowing = list(
        Borrowing.objects.filter(expected_return_date__lt=datetime.date.today())
        .filter(actual_return_date=None)
        .values()
    )
    borrow_list = []
    no_borrowing_message = "No borrowings overdue today!"
    if overdue_borrowing:
        for borrow in overdue_borrowing:
            book = Book.objects.get(id=borrow["book_id"])
            user = User.objects.get(id=borrow["user_id"])
            message = (
                f"Overdue borrowings id {borrow['id']}, "
                f"expected return date {borrow['expected_return_date']}, "
                f"actual return date {borrow['actual_return_date']}, "
                f"client username {user.email}, "
                f"borrow date {borrow['borrow_date']}, "
                f"book: book id {book.id} title '{book.title}' authors {book.authors}, "
                f"daily fee {book.daily_fee}"
            )
            borrow_list.append(message)
        return borrow_list
    return no_borrowing_message
