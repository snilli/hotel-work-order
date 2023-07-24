from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.response import Response
from work_orders.models import MetaStatus, MetaType, Room, WorkOrder
from work_orders.permissions import WorkOrderPermission
from work_orders.serializers import (
    AssingWorkOrderSerializer,
    CancelCleaningWorkOrderSerializer,
    CreateAmenityRequestWorkOrderSerializer,
    CreateCleaningWorkOrderSerializer,
    CreateMaidRequestWorkOrderSerializer,
    CreateTechnicianRequestWorkOrderSerializer,
    FinishWorkOrderSerializer,
    RoomSerializer,
    StartWorkOrderSerializer,
    WorkOrderSerializer,
)


class ReadOnly(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class WorkOrderView(
    # mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    permission_classes = [WorkOrderPermission]

    @action(methods=['post'], detail=False, url_path='create-cleaning')
    def create_cleaning(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        request.data['type'] = MetaType.CLEANING
        return self._create(request, CreateCleaningWorkOrderSerializer)

    @action(methods=['post'], detail=True, url_path='cancel-cleaning')
    def cancel_cleaning(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        request.data['status'] = MetaStatus.CANCEL
        return self._update(request, CancelCleaningWorkOrderSerializer)

    @action(methods=['post'], detail=False, url_path='create-maid-request')
    def create_maid_request(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        request.data['type'] = MetaType.MAID_REQUEST
        return self._create(request, CreateMaidRequestWorkOrderSerializer)

    @action(methods=['post'], detail=False, url_path='create-technician-request')
    def create_technician_request(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        request.data['type'] = MetaType.TECHNICIAN_REQUEST
        return self._create(request, CreateTechnicianRequestWorkOrderSerializer)

    @action(methods=['post'], detail=False, url_path='create-amenity-request')
    def create_amenity_request(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        request.data['type'] = MetaType.AMENITY_REQUEST
        return self._create(request, CreateAmenityRequestWorkOrderSerializer)

    def _create(self, request, serializer_class):

        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path=r'assign/(?P<assignee>[^/.]+)')
    def assign(self, request, assignee=None, *args, **kwargs):
        request.data['assigned_to'] = assignee
        request.data['status'] = MetaStatus.ASSIGNED

        return self._update(request, AssingWorkOrderSerializer)

    @action(methods=['post'], detail=True)
    def start(self, request, *args, **kwargs):
        request.data['started_at'] = datetime.now()
        request.data['status'] = MetaStatus.IN_PROGRESS

        return self._update(request, StartWorkOrderSerializer)

    @action(methods=['post'], detail=True)
    def finish(self, request, *args, **kwargs):
        request.data['finished_at'] = datetime.now()
        request.data['status'] = MetaStatus.DONE

        return self._update(request, FinishWorkOrderSerializer)

    def _update(self, request, serializer_class):
        instance = self.get_object()
        serializer = serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class RoomView(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
