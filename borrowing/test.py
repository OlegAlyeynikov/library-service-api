from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from book.models import Book
from borrowing.models import Borrowing

BORROW_URL = reverse("borrowing-list")


def create_book() -> Book:
    data = {
        "title": "test_title",
        "authors": "test_author",
        "cover": "HARD",
        "inventory": 5,
        "daily_fee": Decimal(10),
    }
    return Book.objects.create(**data)


class BorrowCreateTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        user = get_user_model().objects.create_user(
            "test@test.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(user=user)

    def test_book_inventory(self) -> None:
        book = create_book()
        return_date = date.today() + timedelta(days=10)
        borrow_date = date.today()
        data = {
            "borrow_date": borrow_date,
            "expected_return_date": return_date,
            "book": book.id,
        }
        res = self.client.post(BORROW_URL, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        book = Book.objects.get(id=book.id)
        self.assertEqual(book.inventory, 4)

    def test_return_book(self) -> None:
        book = create_book()
        actual_return_date = date.today() + timedelta(days=15)
        expected_return_date = date.today() + timedelta(days=10)
        borrow_date = date.today()
        borrowing_data = {
            "borrow_date": borrow_date,
            "expected_return_date": expected_return_date,
            "book": book.id,
        }
        res = self.client.post(BORROW_URL, borrowing_data)
        borrowing_ = Borrowing.objects.get(id=1)
        return_url = (
            reverse("borrowing-detail", kwargs={"pk": res.data["id"]}) + "return/"
        )
        return_data = {
            "actual_return_date": actual_return_date,
            "id": borrowing_.id,
        }
        response = self.client.post(return_url, return_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book = Book.objects.get(id=book.id)
        self.assertEqual(book.inventory, 5)
