import collections
import copy
import unittest

from betamax.configure import Configuration
from betamax.cassette import Cassette


class TestConfiguration(unittest.TestCase):
    def setUp(self):
        self.cassette_options = copy.deepcopy(
            Cassette.default_cassette_options
            )
        self.cassette_dir = Configuration.CASSETTE_LIBRARY_DIR

    def tearDown(self):
        Cassette.default_cassette_options = self.cassette_options
        Cassette.hooks = collections.defaultdict(list)
        Configuration.CASSETTE_LIBRARY_DIR = self.cassette_dir

    def test_acts_as_pass_through(self):
        c = Configuration()
        c.default_cassette_options['foo'] = 'bar'
        assert 'foo' in Cassette.default_cassette_options
        assert Cassette.default_cassette_options.get('foo') == 'bar'

    def test_sets_cassette_library(self):
        c = Configuration()
        c.cassette_library_dir = 'foo'
        assert Configuration.CASSETTE_LIBRARY_DIR == 'foo'

    def test_is_a_context_manager(self):
        with Configuration() as c:
            assert isinstance(c, Configuration)

    def test_allows_registration_of_placeholders(self):
        opts = copy.deepcopy(Cassette.default_cassette_options)
        c = Configuration()
        c.define_cassette_placeholder('<TEST>', 'test')

        assert opts != Cassette.default_cassette_options
        placeholders = Cassette.default_cassette_options['placeholders']
        assert placeholders[0]['placeholder'] == '<TEST>'
        assert placeholders[0]['replace'] == 'test'

    def test_registers_pre_record_hooks(self):
        c = Configuration()
        assert Cassette.hooks['before_record'] == []
        c.before_record(callback=lambda: None)
        assert Cassette.hooks['before_record'] != []
        assert len(Cassette.hooks['before_record']) == 1
        assert callable(Cassette.hooks['before_record'][0])

    def test_registers_pre_playback_hooks(self):
        c = Configuration()
        assert Cassette.hooks['before_playback'] == []
        c.before_playback(callback=lambda: None)
        assert Cassette.hooks['before_playback'] != []
        assert len(Cassette.hooks['before_playback']) == 1
        assert callable(Cassette.hooks['before_playback'][0])
