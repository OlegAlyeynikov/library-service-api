from rest_framework import routers

from .views import PaymentView

app_name = "payment"

router = routers.DefaultRouter()
router.register("payments", PaymentView, basename="payment")
urlpatterns = router.urls
