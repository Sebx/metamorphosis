##
# File: entities\instance.py.
#
# Summary:  Instance class.

from metamorphosis.entities.domain_model import DomainModel

class Instance(object):
    def __init__(self, idx, name, route, topics, running):
        self.idx = id
        self.name = name
        self.route = route
        self.topics = topics
        self.running = running

    @classmethod
    def from_dict(cls, adict):
        instance = Instance(
            id=adict["id"],
            name=adict["name"],
            route=adict["route"],
            topics=adict["topics"],
            running=adict["running"]
        )
        return instance

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "route": self.route,
            "topics": self.topics,
            "route": self.running
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

DomainModel.register(Instance)