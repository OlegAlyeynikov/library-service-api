from django.db import transaction
from rest_framework import serializers

from book.serializers import BookSerializer
from borrowing.bot import TelegramBot
from borrowing.models import Borrowing
from payment.models import Payment
from payment.payment import create_payment_session
from payment.serializers import PaymentSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(many=False, read_only=True, slug_field="email")

    def validate(self, attrs) -> None:
        data = super(BorrowingSerializer, self).validate(attrs)
        Borrowing.validate_correct_date(
            attrs["borrow_date"],
            attrs["expected_return_date"],
            serializers.ValidationError,
        )
        if attrs["book"].inventory == 0:
            Borrowing.validate_book_inventory(
                attrs["book"].inventory,
                attrs["book"].title,
                serializers.ValidationError,
            )
        return data

    @transaction.atomic
    def create(self, validated_data: dict) -> Borrowing:
        book = validated_data["book"]
        user = validated_data["user"]

        if book.inventory == 0:
            raise serializers.ValidationError("No requested book in the library!")
        else:
            borrow = super().create(validated_data)
            request = self.context["request"]
            create_payment_session(borrow, "PENDING", request, "PAID")
            payment = Payment.objects.get(borrowing=borrow)
            message = (
                f"{user.first_name} {user.last_name} "
                f"You created new borrowing in the library: "
                f"borrow date {validated_data['borrow_date']}, "
                f"expected return date {validated_data['expected_return_date']}, "
                f"book {validated_data['book']}, "
                f"your link for pay: {payment.session_url}"
            )
            bot = TelegramBot()
            bot.send_message_(message)
            book.inventory -= 1
            book.save()
            return borrow

    def update(self, instance: Borrowing, validated_data: dict) -> Borrowing:
        if instance.borrow_date:
            raise serializers.ValidationError(
                {
                    "error": "You can't change borrowing",
                }
            )
        return super().update(instance, validated_data)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
            "payments",
        )
        read_only_fields = ["user", "actual_return_date", "payments"]


class BorrowDetailSerializer(BorrowingSerializer):
    book = BookSerializer(many=False, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "actual_return_date")
