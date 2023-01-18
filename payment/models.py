from django.db import models

from borrowing.models import Borrowing


class Payment(models.Model):
    STATUS_CHOICES = [("PENDING", "Payment pending"), ("PAID", "Payment paid")]
    # Status PENDING | PAID ОЖИДАНИЕ | ОПЛАЧЕННЫЙ
    TYPE_CHOICES = [("PAYMENT", "Type Payment"), ("FINE", "Type Fine")]
    # Type PAYMENT | FINE ОПЛАТА | ШТРАФ

    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    borrowing = models.ForeignKey(
        Borrowing, on_delete=models.CASCADE, related_name="payments"
    )
    session_url = models.URLField()
    # url to stripe payment session URL для чередования платежного сеанса
    session_id = models.CharField(max_length=63, unique=True)
    # id of stripe payment session идентификатор сеанса оплаты с чередованием
    money_to_pay = models.DecimalField(max_digits=9, decimal_places=2)
    # calculated borrowing total price расчетная общая стоимость займа

    def __str__(self):
        return f"{self.type} {self.status}"
