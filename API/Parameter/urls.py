
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ParameterViewSet

router = DefaultRouter()
router.register(r'parameters', ParameterViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('update/', update),
]