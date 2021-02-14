from rest_framework.routers import DefaultRouter
from . import views

app_name = "rooms"
router = DefaultRouter() #()꼭 붙여주기
router.register("", views.RoomViewSet)

urlpatterns = router.urls
