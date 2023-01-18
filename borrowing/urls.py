from django.urls import path, include
from rest_framework import routers

from borrowing.views import BorrowingViewSet

app_name = "borrowing"


router = routers.DefaultRouter()
router.register("borrowings", BorrowingViewSet)
# router.register("buses", BusViewSet)
# router.register("trips", TripViewSet)
# router.register("orders", OrderViewSet)
# router.register("tickets", TicketViewSet)

urlpatterns = [path("", include(router.urls))]

# 1. POST: borrowings/ - add new borrowing (when borrow book - inventory should be made -= 1)
# 2. GET: borrowings/?user_id=...&is_active=...- get borrowings by user id
# and whether is borrowing still active or not.
# 3. GET: borrowings/<id>/ - get specific borrowing
# 4. POST: borrowings/<id>/return/ - set actual return date (inventory should be made += 1)
