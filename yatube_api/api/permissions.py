from rest_framework import permissions


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):

    # def has_object_permission(self, request, view, obj):
    #     return (
    #         request.method in permissions.SAFE_METHODS
    #         or obj.author == request.user)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user