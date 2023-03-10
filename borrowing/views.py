import datetime

from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from book.models import Book
from borrowing.bot import TelegramBot
from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingReturnSerializer
from payment.models import Payment
from payment.payment import create_payment_session


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        queryset = self.queryset
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if str(self.request.user.id) == user_id and is_active:
            queryset = queryset.filter(actual_return_date=None)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "return_book":
            return BorrowingReturnSerializer
        return BorrowingSerializer

    @transaction.atomic
    @action(methods=["POST"], detail=True, url_path="return")
    def return_book(self, request, pk: int) -> Response:
        """Endpoint for book borrowing return"""
        borrowing = self.get_object()
        if borrowing.actual_return_date is None:
            borrowing.actual_return_date = datetime.date.today()
            borrowing.save()
            book = Book.objects.get(id=borrowing.book.id)
            book.inventory += 1
            book.save()
            delta = datetime.date.today() - borrowing.expected_return_date

            if delta.days > 0:
                create_payment_session(borrowing, "FINE", request, "PENDING")
                payment = Payment.objects.get(borrowing=borrowing)
                message = f"Your link for fine's pay: {payment.session_url}"
                bot = TelegramBot()
                bot.send_message_(message)
                return Response(
                    data="You have to pay fine payment!",
                    status=status.HTTP_402_PAYMENT_REQUIRED,
                )

            serializer = self.get_serializer(borrowing, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_200_OK)

        return Response(
            data="You can't return this book!", status=status.HTTP_400_BAD_REQUEST
        )
