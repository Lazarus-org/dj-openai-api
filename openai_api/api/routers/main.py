from django.urls import path, include
from rest_framework.routers import DefaultRouter
from openai_api.api.views.openai import OpenAIChatViewSet

router = DefaultRouter()
router.register(r"openai_api", OpenAIChatViewSet, basename="openai_api")

urlpatterns = router.urls