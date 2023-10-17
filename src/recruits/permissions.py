from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsManagerOrReadOnly(BasePermission):
    """
    permission class, editable only for manager and read only for users
    """

    def has_permission(self, request, view):
        # post, update, delete for only manager
        return bool(
            request.method in SAFE_METHODS or (request.user and request.user.is_manager)
        )


class IsNotManagerOnlyOrReadOnly(BasePermission):
    """
    permission class, only normal user can post.
    """

    def has_permission(self, request, view):

        return bool(
            request.method in SAFE_METHODS
            or (request.user and not request.user.is_manager)
        )
