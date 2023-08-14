from .abstract_model import AbstractModel
from database.db import db


# Req. 1
class LanguageModel(AbstractModel):
    _collection = db["languages"]

    def __init__(self, dict_data):
        super().__init__(dict_data)

    # Req. 2
    def to_dict(self):
        return {
            'name': self.data['name'],
            'acronym': self.data['acronym'],
        }

    # Req. 3
    @classmethod
    def list_dicts(cls):
        return [cls(data).to_dict() for data in cls._collection.find()]
