from api.utils import failure_response
from api.utils import success_response
from rest_framework import status


class BlockController:
    def __init__(self, request, data, serializer):
        self._request = request
        self._data = data
        self._serializer = serializer

    def block(self, user, blocked_user):
        """Block `blocked_user` for `user`."""
        if blocked_user not in user.blocked_users.all():
            user.blocked_users.add(blocked_user)
        user.save()
        return user, status.HTTP_200_OK

    def unblock(self, user, blocked_user):
        """Unblock `blocked_user` for `user`."""
        if blocked_user in user.blocked_users.all():
            user.blocked_users.remove(blocked_user)
        user.save()
        return user, status.HTTP_200_OK

    def get_blocked_users(self, user):
        """Get blocked users for `user`."""
        return user.blocked_users.all()

    def get_if_blocked(self, user, blocked_user):
        """Get if `blocked_user` is blocked for `user`."""
        return blocked_user in user.blocked_users.all()

    def process(self):
        """Process the request."""
        serializer = self._serializer(data=self._data)
        if not serializer.is_valid():
            return failure_response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        if serializer.validated_data.get("blocked_user") == self._request.user:
            return failure_response(
                {"error": "Cannot block yourself."}, status.HTTP_400_BAD_REQUEST
            )
        if serializer.validated_data.get("blocked_user") in self.get_blocked_users(
            self._request.user
        ):
            return failure_response(
                {"error": "User already blocked."}, status.HTTP_400_BAD_REQUEST
            )
        blocked_user = serializer.validated_data.get("blocked_user")
        user, status_code = self.block(self._request.user, blocked_user)
        if status_code != status.HTTP_200_OK:
            return failure_response(
                {"error": "Unable to block user."}, status.HTTP_400_BAD_REQUEST
            )
        return success_response(self._serializer(user).data, status.HTTP_200_OK)
