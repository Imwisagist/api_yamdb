from rest_framework import permissions


class OwnerCheck(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (request.method in permissions.SAFE_METHODS
                or obj.author == user
                or user.permission == 'admin'
                or user.permission == 'moderator'
                )
