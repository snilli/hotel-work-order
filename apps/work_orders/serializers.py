from rest_framework import serializers
from work_orders.models import (
    MetaAmenityType,
    MetaDefectType,
    MetaStatus,
    MetaType,
    Room,
    WorkOrder,
)


class WorkOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkOrder
        fields = '__all__'


# - Maid Supervisor
#   - Create Cleaning
#   - Create Maid Request
# - Guest
#   - Cancel Cleaning
#   - Create Technician Request
#   - Create Amenity Request
# - Supervisor
#   - Create Technician Request


# {
#   "type": "Maid Request",
#   "status": "Created",
#   "created_by": 2,
#   "room": 1
# }
class CreateCleaningWorkOrderSerializer(WorkOrderSerializer):
    type = serializers.ChoiceField(MetaType.choices)


class CreateMaidRequestWorkOrderSerializer(WorkOrderSerializer):
    type = serializers.ChoiceField(MetaType.choices)
    description = serializers.CharField(required=False)


class CreateTechnicianRequestWorkOrderSerializer(WorkOrderSerializer):
    type = serializers.ChoiceField(MetaType.choices)
    defect_type = serializers.ChoiceField(MetaDefectType.choices)


class CreateAmenityRequestWorkOrderSerializer(WorkOrderSerializer):
    type = serializers.ChoiceField(MetaType.choices)
    amenity_type = serializers.ChoiceField(MetaAmenityType.choices)
    amenity_qty = serializers.IntegerField()


class AssingWorkOrderSerializer(WorkOrderSerializer):

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class StartWorkOrderSerializer(WorkOrderSerializer):

    def update(self, instance, validated_data):
        if instance.started_at and validated_data.get('started_at'):
            raise serializers.ValidationError({'started_at', 'Work Order Already Starded'})
        return super().update(instance, validated_data)


class CancelCleaningWorkOrderSerializer(WorkOrderSerializer):

    def update(self, instance, validated_data):
        if instance.status == MetaStatus.CANCEL:
            raise serializers.ValidationError({'status', 'Work Order Already Canceled'})
        if instance.type != MetaType.CLEANING:
            raise serializers.ValidationError({'type', 'Work Order Not Cleaning Type'})
        return super().update(instance, validated_data)


class FinishWorkOrderSerializer(WorkOrderSerializer):

    def update(self, instance, validated_data):
        if instance.started_at is None and validated_data.get('finished_at'):
            raise serializers.ValidationError({'finished_at': 'Work Order Should Start Befor Action Finish'})
        elif instance.finished_at and validated_data.get('finished_at'):
            raise serializers.ValidationError({'finished_at': 'Work Order Already Finished'})
        return super().update(instance, validated_data)


class RoomSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return super().create(validated_data)

    class Meta:
        model = Room
        fields = '__all__'