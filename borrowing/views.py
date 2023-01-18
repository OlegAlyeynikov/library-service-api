from rest_framework import viewsets

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer


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


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
