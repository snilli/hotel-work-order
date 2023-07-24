from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from work_orders.models import WorkOrder


def get_perm(action: str):
    return f"work_orders.{permissions_detail[action]['codename']}"


permissions_detail = {
    'create_cleaning': {
        'name': 'Create Cleaning',
        'codename': 'create_cleaning',
    },
    'create_maid_request': {
        'name': 'Create Maid Request',
        'codename': 'create_maid_request',
    },
    'create_amenity_request': {
        'name': 'Create Amenity Request',
        'codename': 'create_amenity_request',
    },
    'create_technician_request': {
        'name': 'Create Technician Request',
        'codename': 'create_technician_request',
    },
    'cancel_cleaning': {
        'name': 'Cancel Cleaning',
        'codename': 'cancel_cleaning',
    }
}

groups_detail = [
    {
        'name': 'Maid Supervisor',
        'permission_index': [0, 1],
    },
    {
        'name': 'Guest',
        'permission_index': [2, 3, 4],
    },
    {
        'name': 'Supervisor',
        'permission_index': [3],
    },
]


class Command(BaseCommand):
    help = "Init User Group To App"

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(WorkOrder)
        permissions = list(
            map(
                lambda res: res[0],
                [
                    Permission.objects.get_or_create(
                        name=permission['name'],
                        codename=permission['codename'],
                        defaults={
                            "content_type": content_type,
                        },
                    ) for _,
                    permission in permissions_detail.items()
                ]
            )
        )

        for group_detail in groups_detail:
            group, created = Group.objects.get_or_create(name=group_detail['name'],)
            if not created:
                for permission_index in group_detail['permission_index']:
                    group.permissions.add(permissions[permission_index])
