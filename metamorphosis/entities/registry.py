##
# File: entities\registry.py.
#
# Summary:  Registry class.

from metamorphosis.entities.domain_model import DomainModel

class Registry(object):
    def __init__(self, idx, code_id, instance_id, start_date, stop_date):
        self.id = idx
        self.code_id = code_id
        self.instance_id = instance_id
        self.start_date = start_date
        self.stop_date = stop_date

    @classmethod
    def from_dict(cls, adict):
        instance = Registry(
            id=adict["id"],
            code_id=adict["code_id"],
            instance_id=adict["instance_id"],
            start_date=adict["start_date"],
            stop_date=adict["stop_date"]
        )
        return instance

    def to_dict(self):
        return {
            "id": self.id,
            "code_id": self.code_id,
            "instance_id": self.instance_id,
            "start_date": self.start_date,
            "stop_date": self.stop_date
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

DomainModel.register(Registry)