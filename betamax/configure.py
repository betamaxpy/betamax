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

    def define_cassette_placeholder(self, placeholder, replace):
        """Define a placeholder value for some text.

        This also will replace the placeholder text with the text you wish it
        to use when replaying interactions from cassettes.

        :param str placeholder: (required), text to be used as a placeholder
        :param str replace: (required), text to be replaced or replacing the
            placeholder
        """
        self.default_cassette_options['placeholders'].append({
            'placeholder': placeholder,
            'replace': replace
        })
