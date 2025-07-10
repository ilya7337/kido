from rest_framework import permissions

class IsTrainerOrManager(permissions.BasePermission):
    """
    Доступ разрешён только пользователям с ролью 'trainer'
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (getattr(request.user, 'role', None) == 'trainer' or getattr(request.user, 'role', None) == 'manager')

class IsTrainerManagerOrAdmin(permissions.BasePermission):
    """
    Доступ разрешён только пользователям с ролью 'trainer', 'manager' или 'admin'
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            getattr(request.user, 'role', None) in ['trainer', 'manager', 'admin']
        )