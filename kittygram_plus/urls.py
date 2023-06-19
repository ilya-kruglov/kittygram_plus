from django.urls import include, path

from rest_framework.routers import DefaultRouter

from cats.views import CatViewSet, OwnerViewSet


router = DefaultRouter()
router.register('cats', CatViewSet, basename='cat')
router.register('owners', OwnerViewSet, basename='owner')

urlpatterns = [
    path('', include(router.urls)),
]
