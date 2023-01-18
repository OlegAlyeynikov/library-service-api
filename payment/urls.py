from django.urls import path, include
from rest_framework import routers

from payment.views import PaymentViewSet

app_name = "payment"


router = routers.DefaultRouter()
router.register("payments", PaymentViewSet)
# router.register("buses", BusViewSet)
# router.register("trips", TripViewSet)
# router.register("orders", OrderViewSet)
# router.register("tickets", TicketViewSet)

urlpatterns = [path("", include(router.urls))]
