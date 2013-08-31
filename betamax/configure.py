from betamax.cassette import Cassette


class Configuration(object):
    CASSETTE_LIBRARY_DIR = 'vcr/cassettes'

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    @property
    def cassette_library_dir(self):
        return Configuration.CASSETTE_LIBRARY_DIR

    @cassette_library_dir.setter
    def cassette_library_dir(self, value):
        Configuration.CASSETTE_LIBRARY_DIR = value

    @property
    def default_cassette_options(self):
        return Cassette.default_cassette_options

    @default_cassette_options.setter
    def default_cassette_options(self, value):
        Cassette.default_cassette_options = value
