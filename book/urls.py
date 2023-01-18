from django.urls import path, include
from rest_framework import routers

from book.views import BookViewSet

app_name = "book"


router = routers.DefaultRouter()
router.register("books", BookViewSet)
# router.register("buses", BusViewSet)
# router.register("trips", TripViewSet)
# router.register("orders", OrderViewSet)
# router.register("tickets", TicketViewSet)

urlpatterns = [path("", include(router.urls))]
