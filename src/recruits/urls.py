from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"", views.RecruitViewSet, basename="recruits")

urlpatterns = router.urls
