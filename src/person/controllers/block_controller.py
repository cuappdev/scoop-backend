from api.utils import failure_response
from api.utils import success_response
from rest_framework import status

from ..models import User


class BlockController:
    def __init__(self, user, data, serializer):
        self._user = user
        self._data = data
        self._serializer = serializer

    def block(self, user, blocked_user):
        """Block `blocked_user` for `user`."""
        person = user.person
        if blocked_user.person not in person.blocked_users.all():
            person.blocked_users.add(blocked_user.person)
        person.save()
        return user, status.HTTP_200_OK

    def get_blocked_users(self, user):
        """Get blocked users for `user`."""
        return user.person.blocked_users.all()

    def get_if_blocked(self, user, blocked_user):
        """Get if `blocked_user` is blocked for `user`."""
        return blocked_user in user.person.blocked_users.all()

    def process(self):
        """Process the request."""
        try:
            blocked_user = User.objects.get(id=self._data.get("blocked_user"))
        except User.DoesNotExist:
            return failure_response(
                {"error": "User does not exist."}, status.HTTP_400_BAD_REQUEST
            )
        if blocked_user.id == self._user.id:
            return failure_response(
                {"error": "Cannot block yourself."}, status.HTTP_400_BAD_REQUEST
            )
        if blocked_user in self.get_blocked_users(
            self._user
        ):
            return failure_response(
                {"error": "User already blocked."}, status.HTTP_400_BAD_REQUEST
            )
        user, status_code = self.block(self._user, blocked_user)
        if status_code != status.HTTP_200_OK:
            return failure_response(
                {"error": "Unable to block user."}, status.HTTP_400_BAD_REQUEST
            )
        return success_response(self._serializer(user).data, status.HTTP_200_OK)


class UnblockController:
    def __init__(self, user, data, serializer):
        self._user = user
        self._data = data
        self._serializer = serializer

    def get_blocked_users(self, user):
        """Get blocked users for `user`."""
        return user.person.blocked_users.all()

    def unblock(self, user, unblocked_user):
        """Unblock `blocked_user` for `user`."""
        person = user.person
        # if unblocked_user in person.blocked_users.all():
        #     person.blocked_users.remove(unblocked_user)
        person.blocked_users.remove(unblocked_user.person)
        person.save()
        return user, status.HTTP_200_OK

    def process(self):
        """Process the request."""
        try:
            unblocked_user = User.objects.get(id=self._data.get("unblocked_user"))
        except User.DoesNotExist:
            return failure_response(
                {"error": "User does not exist."}, status.HTTP_400_BAD_REQUEST
            )
        if unblocked_user.id == self._user.id:
            return failure_response(
                {"error": "Cannot unblock yourself."}, status.HTTP_400_BAD_REQUEST
            )
        user, status_code = self.unblock(self._user, unblocked_user)
        if status_code != status.HTTP_200_OK:
            return failure_response(
                {"error": "Unable to unblock user."}, status.HTTP_400_BAD_REQUEST
            )
        return success_response(self._serializer(user).data, status.HTTP_200_OK)
