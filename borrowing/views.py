from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingReturnSerializer


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

    @action(methods=["POST"], detail=True, url_path="return")
    def return_book(self, request, pk=None):
        """Endpoint for book borrowing return"""
        borrowing = self.get_object()
        serializer = self.get_serializer(borrowing, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class BorrowingReturnView(generics.RetrieveUpdateAPIView):
#     queryset = Borrowing.objects.all()
#     serializer_class = BorrowingSerializer
#     # authentication_classes = (TokenAuthentication, )
#     # permission_classes = (IsAuthenticated, )
#
#     def get_queryset(self):
#         queryset = self.queryset
#         if not self.request.user.is_staff:
#             queryset = queryset.filter(user=self.request.user)
#
#         id = self.request.query_params.get("id")
#         is_active = self.request.query_params.get("is_active")
#
#         if str(self.request.user.id) == user_id and is_active:
#             queryset = queryset.filter(actual_return_date=None)
#
#         return queryset


# class SnippetHighlight(generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     renderer_classes = [renderers.StaticHTMLRenderer]
#
#     def get(self, request, *args, **kwargs):
#         snippet = self.get_object()
#         return Response(snippet.highlighted)
