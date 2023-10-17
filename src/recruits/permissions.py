from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)


class IsManagerOrReadOnly(BasePermission):
    """
    permission class, editable only for manager and read only for users
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or (request.user and getattr(request.user, "is_manager", False))
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or (
                request.user and (getattr(obj.company, "manager", None) == request.user)
            )
        )


class IsNotManagerOnlyOrReadOnly(BasePermission):
    """
    permission class, only normal user can post.
    """

    def has_permission(self, request, view):

        return bool(
            request.method in SAFE_METHODS
            or (
                request.user
                and request.user.is_authenticated
                and not getattr(request.user, "is_manager", False)
            )
        )
