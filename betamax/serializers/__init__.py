# -*- coding: utf-8 -*-

serializer_registry = {}

from .base import BaseSerializer
from .json_serializer import JSONSerializer
from .proxy import SerializerProxy

_serializers = [JSONSerializer]
serializer_registry.update(dict((s.name, s()) for s in _serializers))
del _serializers

__all__ = ['BaseSerializer', 'JSONSerializer', 'SerializerProxy']
