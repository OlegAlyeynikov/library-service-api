from rest_framework import viewsets

from book.models import Book
from book.serializers import BookSerializer


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


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
