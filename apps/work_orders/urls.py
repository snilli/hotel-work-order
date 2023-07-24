from rest_framework import routers
from work_orders.views import RoomView, WorkOrderView

router = routers.DefaultRouter()
router.register('work-orders', WorkOrderView)
router.register('rooms', RoomView)

urlpatterns = router.urls