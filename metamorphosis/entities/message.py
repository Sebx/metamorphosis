from entities.domain_model import DomainModel


class Message(object):

  def __init__(self, id, topic, value):
        self.id = id
        self.topic = topic
        self.value = value

    @classmethod
    def from_dict(cls, adict):
        message = Message(
            id=adict['id'],
            topic=adict['topic'],
            value=adict['value']
        )

        return message

    def to_dict(self):
        return {
            'id': self.id,
            'topic': self.topic,
            'value': self.value
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()


DomainModel.register(Message)
