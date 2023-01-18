from rest_framework import viewsets

from payment.models import Payment
from payment.serializers import PaymentSerializer


# class BusViewSet(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     viewsets.GenericViewSet
# ):    # viewsets.ModelViewSet
#
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer
#     permission_classes = (IsAdminOrAuthenticatedReadOnly, )


# class BookListView(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
