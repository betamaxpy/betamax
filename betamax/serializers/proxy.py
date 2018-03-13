# -*- coding: utf-8 -*-
from .base import BaseSerializer
from betamax.exceptions import MissingDirectoryError

import os


class SerializerProxy(BaseSerializer):

    """
    This is an internal implementation detail of the betamax library.

    No users implementing a serializer should be using this. Developers
    working on betamax need only understand that this handles the logic
    surrounding whether a cassette should be updated, overwritten, or created.

    It provides one consistent way for betamax to be confident in how it
    serializes the data it receives. It allows authors of Serializer classes
    to not have to duplicate how files are handled. It delegates the
    responsibility of actually serializing the data to those classes and
    handles the rest.

    """

    def __init__(self, serializer, cassette_path, allow_serialization=False):
        self.proxied_serializer = serializer
        self.allow_serialization = allow_serialization
        self.cassette_path = cassette_path

    def _ensure_path_exists(self):
        directory, _ = os.path.split(self.cassette_path)
        if not (directory == '' or os.path.isdir(directory)):
            raise MissingDirectoryError(
                'Configured cassette directory \'{0}\' does not exist - try '
                'creating it'.format(directory)
                )
        if not os.path.exists(self.cassette_path):
            open(self.cassette_path, 'w+').close()

    @classmethod
    def find(cls, serialize_with, cassette_library_dir, cassette_name):
        from . import serializer_registry
        serializer = serializer_registry.get(serialize_with)
        if serializer is None:
            raise ValueError(
                'No serializer registered for {0}'.format(serialize_with)
                )

        cassette_path = cls.generate_cassette_name(
            serializer, cassette_library_dir, cassette_name
            )
        return cls(serializer, cassette_path)

    @staticmethod
    def generate_cassette_name(serializer, cassette_library_dir,
                               cassette_name):
        return serializer.generate_cassette_name(
            cassette_library_dir, cassette_name
            )

    def serialize(self, cassette_data):
        if not self.allow_serialization:
            return

        self._ensure_path_exists()

        write_mode = getattr(self.proxied_serializer, 'write_mode', 'w')
        with open(self.cassette_path, write_mode) as fd:
            fd.write(self.proxied_serializer.serialize(cassette_data))

    def deserialize(self):
        self._ensure_path_exists()

        read_mode = getattr(self.proxied_serializer, 'read_mode', 'r')
        with open(self.cassette_path, read_mode) as fd:
            data = self.proxied_serializer.deserialize(fd.read())

        return data
