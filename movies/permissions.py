from rest_framework.permissions import SAFE_METHODS, BasePermission


def user_type(user):
    if user.is_staff is True and user.is_superuser is False:
        return 'critic'

    if user.is_staff is True and user.is_superuser is True:
        return 'admin'


class OnlyUser(BasePermission):
    def has_permission(self, request, views):
        user = request.user

        if not user.is_staff and not user.is_superuser:
            return True


class OnlyAdmin(BasePermission):
    def has_permission(self, request, view):
        user = user_type(request.user)

        if request.method in SAFE_METHODS:
            return True

        # if request.method == 'POST' or request.method == 'DELETE':
        return True if user == 'admin' else False


class OnlyCritico(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        return user.is_staff is True
