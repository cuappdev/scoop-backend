from api.utils import success_response

from ..models import Request


class GetUserRequestsController:
    def __init__(self, request, user, serializer):
        self._request = request
        self._user = user
        self._serializer = serializer

    def process(self):
        awaiting_approval = Request.objects.filter(
            approver=self._user, approved=None
        ).order_by("timestamp")
        pending_requests = Request.objects.filter(
            approvee=self._user, approved=None
        ).order_by("timestamp")

        return success_response(
            {
                "awaiting_approval": self._serializer(
                    awaiting_approval, many=True
                ).data,
                "pending_requests": self._serializer(pending_requests, many=True).data,
            }
        )
