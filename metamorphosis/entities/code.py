from entities.domain_model import DomainModel


class Code(object):

    def __init__(self, id, language, language_version, dependencies, source_code):
        self.id = id
        self.language = language
        self.language_version = language_version
        self.dependencies = dependencies
        self.source_code = source_code

    @classmethod
    def from_dict(cls, adict):
        code = Code(
            id=adict['id'],
            language=adict['language'],
            language_version=adict['language_version'],
            dependencies=adict['dependencies'],
            source_code=adict['source_code'],
        )
        return code

    def to_dict(self):
        return {
            'id': self.id,
            'language': self.language,
            'language_version': self.language_version,
            'dependencies': self.dependencies,
            'source_code': self.source_code,
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()


DomainModel.register(Code)
