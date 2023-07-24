from django.contrib.auth.models import User
from django.db import models


class Room(models.Model):
    id = models.BigAutoField(
        primary_key=True,
        unique=True,
        editable=False,
    )
    name = models.CharField(blank=False, null=False)


class MetaType(models.TextChoices):
    CLEANING = 'Cleaning',
    MAID_REQUEST = 'Maid Request'
    TECHNICIAN_REQUEST = 'Technician Request'
    AMENITY_REQUEST = 'Amenity Request'


class MetaStatus(models.TextChoices):
    CREATED = 'Created',
    ASSIGNED = 'Assigned'
    IN_PROGRESS = 'In Progress'
    DONE = 'Done'
    CANCEL = 'Cancel'


class MetaDefectType(models.TextChoices):
    ELECTRICITY = 'Electricity',
    AIR_CON = 'Air Con'
    PLUMBING = 'Plumbing'
    INTERNET = 'Internet'


class MetaAmenityType(models.TextChoices):
    SOAP = 'Soap',
    TOWEL = 'Towel'
    SHOWER_CAP = 'Shower Cap'
    RAZOR = 'Razor'


class WorkOrder(models.Model):

    id = models.BigAutoField(
        primary_key=True,
        unique=True,
        editable=False,
    )
    created_by = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='created_by_%(class)s',
    )
    assigned_to = models.ForeignKey(
        User,
        models.CASCADE,
        related_name='assigned_to_%(class)s',
        blank=True,
        null=True,
    )
    room = models.ForeignKey(Room, models.CASCADE)
    started_at = models.DateTimeField(null=True, blank=True, default=None)
    finished_at = models.DateTimeField(null=True, blank=True, default=None)
    type = models.CharField(choices=MetaType.choices)
    defect_type = models.CharField(
        choices=MetaDefectType.choices,
        blank=True,
        null=True,
    )
    amenity_type = models.CharField(
        choices=MetaAmenityType.choices,
        blank=True,
        null=True,
    )
    amenity_qty = models.IntegerField(
        blank=True,
        null=True,
    )
    status = models.CharField(choices=MetaStatus.choices, default=MetaStatus.CREATED)
    description = models.CharField(
        blank=True,
        null=True,
    )
