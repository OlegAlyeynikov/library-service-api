"""library_service_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers
from book.urls import router as book_router
from borrowing.urls import router as borrow_router
from payment.urls import router as payment_router


router = routers.DefaultRouter()
router.registry.extend(book_router.registry)
router.registry.extend(borrow_router.registry)
router.registry.extend(payment_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("user/", include("user.urls", namespace="user")),
    path("api/doc/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
