import copy
import unittest

from betamax.configure import Configuration
from betamax.new_cassette import NewCassette


class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.cassette_options = copy.deepcopy(
            NewCassette.default_cassette_options
            )
        self.cassette_dir = Configuration.CASSETTE_LIBRARY_DIR

    def tearDown(self):
        NewCassette.default_cassette_options = self.cassette_options
        Configuration.CASSETTE_LIBRARY_DIR = self.cassette_dir

    def test_acts_as_pass_through(self):
        c = Configuration()
        c.default_cassette_options['foo'] = 'bar'
        assert 'foo' in NewCassette.default_cassette_options
        assert NewCassette.default_cassette_options.get('foo') == 'bar'

    def test_sets_cassette_library(self):
        c = Configuration()
        c.cassette_library_dir = 'foo'
        assert Configuration.CASSETTE_LIBRARY_DIR == 'foo'

    def test_is_a_context_manager(self):
        with Configuration() as c:
            assert isinstance(c, Configuration)

    def test_allows_registration_of_placeholders(self):
        opts = copy.deepcopy(NewCassette.default_cassette_options)
        c = Configuration()

        c.define_cassette_placeholder('<TEST>', 'test')
        assert opts != NewCassette.default_cassette_options
        placeholders = NewCassette.default_cassette_options['placeholders']
        assert placeholders[0]['placeholder'] == '<TEST>'
        assert placeholders[0]['replace'] == 'test'
