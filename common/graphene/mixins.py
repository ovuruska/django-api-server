from typing import Any, Optional

from django.db.models import Model
from graphene import ResolveInfo
from .permissions import AllowAny

class AuthNode:
    """
    Permission mixin for queries (nodes).
    Allows for simple configuration of access to nodes via class system.
    """

    permission_classes = (AllowAny,)

    @classmethod
    def get_node(cls, info: ResolveInfo, id: str) -> Optional[Model]:
        if all((perm.has_node_permission(info, id) for perm in cls.permission_classes)):
            try:
                object_instance = cls._meta.model.objects.get(pk=id)  # type: ignore
            except cls._meta.model.DoesNotExist:  # type: ignore
                object_instance = None
            return object_instance
        else:
            return None


class AuthMutation:
    """
    Permission mixin for ClientIdMutation.
    """

    permission_classes = (AllowAny,)

    @classmethod
    def has_permission(cls, root: Any, info: ResolveInfo, input: dict) -> bool:
        return all(
            (
                perm.has_mutation_permission(root, info, input)
                for perm in cls.permission_classes
            )
        )
