import datetime
import os

import dotenv

from book.models import Book
from borrowing.models import Borrowing
from library_service_api.settings import BASE_DIR
from user.models import User

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def get_books_with_overdue_borrow():
    overdue_borrowing = (
        Borrowing.objects.filter(expected_return_date__lt=datetime.date.today())
        .filter(actual_return_date=None)
        .values()
    )
    overdue_borrowing_list = list(overdue_borrowing)
    borrow_list = []
    no_borrowing_message = "No borrowings overdue today!"
    if overdue_borrowing:
        for borrow in overdue_borrowing_list:
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
    return borrow_list.append(no_borrowing_message)
