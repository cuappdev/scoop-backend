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


def update_many_to_many_set(class_name, existing_set, ids):
    """Update a ManyToMany relation set for any object"""
    if ids is not None:
        new_objects = []
        for id in ids:
            new_object = class_name.objects.filter(id=id)
            if not new_object:
                return failure_response(
                    f"{class_name.__name__} id {id} does not exist."
                )
            new_objects.append(new_object[0])
        existing_set.set(new_objects)
