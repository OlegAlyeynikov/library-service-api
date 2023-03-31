from datetime import date
from decimal import Decimal

import stripe
from django.conf import settings
from django.http import HttpRequest
from django.urls import reverse

from borrowing.models import Borrowing
from .models import Payment


def calculate_payment(
    expected_return_date: date,
    actual_return_date: date,
    daily_fee: Decimal,
) -> Decimal:

    if actual_return_date:
        delta = actual_return_date - expected_return_date
        return Decimal(daily_fee * Decimal(delta.days) * settings.FINE_MULTIPLIER)

    delta = expected_return_date - date.today()
    return Decimal(daily_fee * Decimal(delta.days))


def create_payment_session(
    borrow: Borrowing,
    payment_type: Payment.type,
    request: HttpRequest,
    payment_status: Payment.status,
) -> None:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    url = reverse("payment-success-url")
    success_url = (
        request.build_absolute_uri(url)[:-1] + "?session_id={CHECKOUT_SESSION_ID}"
    )
    cancel_url = request.build_absolute_uri(reverse("payment-cancel-url"))

    money_to_pay = calculate_payment(
        borrow.expected_return_date,
        borrow.actual_return_date,
        borrow.book.daily_fee,
    )

    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": f"{borrow.book.title}",
                    },
                    "unit_amount": int(money_to_pay) * 100,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )

    Payment.objects.create(
        status=payment_status,
        type=payment_type,
        borrowing=borrow,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=money_to_pay,
    )
