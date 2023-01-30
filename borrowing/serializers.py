import datetime

from rest_framework import serializers


from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
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

    def update(self, instance, validated_data):
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
        )
        read_only_fields = ["actual_return_date"]


class BorrowingReturnSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        if instance.actual_return_date:
            raise serializers.ValidationError(
                {
                    "error": "You can't return a book twice",
                }
            )

        return super().update(instance, validated_data)

    # def validate_actual_return_date(self):
    # if not self.instance and not value:      ## Creation and value not provided
    #     raise serializers.ValidationError('The username is required on user profile creation.')
    # if value and self.instance != value:  ## Update and value differs from existing
    # if self.instance:
    #     raise serializers.ValidationError(
    #         {"error": "You can't return a book twice"}
    #     )
    # raise serializers.ValidationError('The username cannot be modified.')

    # def validate(self, attrs):
    #     data = super(BorrowingReturnSerializer, self).validate(attrs)
    #     if self.instance:
    #         print(self.instance)
    #         print(attrs["actual_return_date"])
    #         print(data)
    #         print(attrs)
    #
    #         raise serializers.ValidationError(
    #             {"error": "You can't return a book twice"}
    #         )
    #
    #     if attrs["actual_return_date"]:
    #
    #         return data

    class Meta:
        model = Borrowing
        fields = ("id", "actual_return_date")

    # def create(self, validated_data):
    #     # book_data = validated_data.pop("book")
    #     borrowing = Borrowing.objects.create(**validated_data)
    #     # for book_data in books_data:
    #     borrowing.book.reduce_inventory_book()
    #     return borrowing
