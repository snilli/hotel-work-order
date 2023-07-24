from rest_framework import permissions
from work_orders.management.commands.init_role import (
    get_perm,
    permissions_detail,
)


class WorkOrderPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if permissions_detail.get(view.action):
            return True if request.user.has_perm(get_perm(view.action)) else False
        return True
