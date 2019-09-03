import json


class CodeEncoder(json.JSONEncoder):
    
    def default(self, o):
        try:
            to_serialize = {
                'id': str(o.id),
                'language': o.language,
                'language_version': o.language_version,
                "dependencies": o.dependencies,
                "source_code": o.source_code,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)