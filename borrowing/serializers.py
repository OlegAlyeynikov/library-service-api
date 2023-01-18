from rest_framework import serializers

from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    # book_id = serializers.IntegerField(source="book.id", read_only=True)
    # costumer_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            # "user",
            # "book_id",
            # "costumer_id",
        )
