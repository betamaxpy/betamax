# -*- coding: utf-8 -*-
from .base import BaseSerializer
from .json_serializer import JSONSerializer
from .pickle_serializer import PickleSerializer
from .proxy import SerializerProxy

serializer_registry = {}

_serializers = [JSONSerializer, PickleSerializer]
serializer_registry.update(dict((s.name, s()) for s in _serializers))
del _serializers

__all__ = ('BaseSerializer', 'JSONSerializer', 'SerializerProxy')
