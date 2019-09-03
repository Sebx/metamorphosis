from entities.domain_model import DomainModel

class Instance(object):
    def __init__(self, id, topic, value):
        self.id = id
        self.name = name
        self.route = route

    @classmethod
    def from_dict(cls, adict):
        instance = Instance(
            id=adict['id'],
            name=adict['name'],
            route=adict['route']
        )

        return instance

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.topic,
            'route': self.value
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

DomainModel.register(Instance)