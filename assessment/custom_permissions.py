from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

from rest_framework.permissions import BasePermission

class IsOwnerOrSuperUser(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.owner == request.user