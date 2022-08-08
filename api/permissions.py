from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrAuthenticatedReadOnly(BasePermission):

    # read (detail/list) | update(PUT/PATCH) | create | delete
    # сначала вызывается этот метод при проверке
    def has_permission(self, request, view):
        """
            Доступ разрушён в если клиент аутентифицирован
        """
        print('\n\n\nhas_permission\n\n\n')
        return request.user.is_authenticated

    # read (detail) | update(PUT/PATCH) | delete
    # и только после has_permission вызывается этот метод
    def has_object_permission(self, request, view, obj):
        """
            Доступ разрушён в 3х случаях:
            1 - клиент автор поста
            2 - клиент админ
            3 - HTTP метод - GET | HEAD | OPTIONS
            Т.е. если не админ и не автор поста, то изменять и удалять нельзя
        """
        print('\n\n\nhas_object_permission\n\n\n')
        return bool(request.user == obj.author
                    or request.user.is_admin
                    or request.method in SAFE_METHODS)
