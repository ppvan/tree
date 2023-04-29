import json

from django.core.serializers import serialize
from django.db.models.query import QuerySet


class ModelSerializer:
    def __init__(self, queryset):
        self.queryset = queryset

    def to_dict(self):
        """
        Convert the model object to a Python dictionary
        """
        if isinstance(self.queryset, QuerySet):
            return json.loads(serialize("json", self.queryset))
        return json.loads(serialize("json", [self.queryset]))[0]["fields"]
