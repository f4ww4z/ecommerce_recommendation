from rest_framework import permissions


class IsUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the current user to modify their own profile
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user


class IsSeller(permissions.BasePermission):
    """
    Custom permission to only allow the current seller to modify their products
    """

    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user


class IsBuyer(permissions.BasePermission):
    """
    Custom permission to only allow the current buyer to modify their orders
    """

    def has_object_permission(self, request, view, obj):
        return obj.buyer == request.user
