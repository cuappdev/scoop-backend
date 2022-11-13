from rest_framework import status
from rest_framework.response import Response


def success_response(data=None, status=status.HTTP_200_OK):
    """Returns a response with `status` (200 default) and `data` if provided."""
    if data is None:
        return Response(status=status)
    return Response(data, status=status)


def failure_response(message=None, status=status.HTTP_404_NOT_FOUND):
    """Returns a response with `status` (404 default) and `message` if provided."""
    if message is None:
        return Response(status=status)
    return Response({"error": message}, status=status)


def update(model, attr_name, attr_value):
    """Update attribute attr_name with attr_value if attr_value isn't None and different from current value."""
    if (
        attr_value is not None
        and attr_value != "null"
        and attr_value != getattr(model, attr_name)
    ):
        setattr(model, attr_name, attr_value)

def modify_attribute(model, attr_name, attr_value):
    """Modify an attribute if it isn't None and has been changed."""
    if (
        attr_value is not None
        and attr_value != "null"
        and attr_value != getattr(model, attr_name)
    ):
        setattr(model, attr_name, attr_value)