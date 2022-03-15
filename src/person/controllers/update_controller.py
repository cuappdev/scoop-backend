from api.utils import success_response
from api.utils import update


class UpdatePersonController:
    def __init__(self, user, data, serializer):
        self._data = data
        self._serializer = serializer
        self._user = user
        self._person = self._user.person

    def process(self):
        netid = self._data.get("netid")
        first_name = self._data.get("first_name")
        last_name = self._data.get("last_name")
        grade = self._data.get("grade")
        phone_number = self._data.get("phone_number")
        pronouns = self._data.get("pronouns")

        update(self._person, "netid", netid)
        update(self._user, "first_name", first_name)
        update(self._user, "last_name", last_name)
        update(self._person, "grade", grade)
        update(self._person, "phone_number", phone_number)
        update(self._person, "pronouns", pronouns)
        self._user.save()
        self._person.save()
        return success_response(self._serializer(self._user).data)
