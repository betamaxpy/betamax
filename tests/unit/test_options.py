import unittest
from itertools import permutations
from betamax.options import Options, validate_record, validate_matchers


class TestValidators(unittest.TestCase):
    def test_validate_record(self):
        for mode in ['once', 'none', 'all', 'new_episodes']:
            assert validate_record(mode) is True

    def test_validate_matchers(self):
        matchers = ['method', 'uri', 'query', 'host', 'body']
        for i in range(1, len(matchers)):
            for l in permutations(matchers, i):
                assert validate_matchers(l) is True

        matchers.append('foobar')
        assert validate_matchers(matchers) is False


class TestOptions(unittest.TestCase):
    def setUp(self):
        self.data = {
            're_record_interval': 10000,
            'match_requests_on': ['method'],
            'serialize': 'json'
        }
        self.options = Options(self.data)

    def test_data_is_valid(self):
        for key in self.data:
            assert key in self.options

    def test_invalid_data_is_removed(self):
        data = self.data.copy()
        data['fake'] = 'value'
        options = Options(data)

        for key in self.data:
            assert key in options

        assert 'fake' not in options

    def test_values_are_validated(self):
        assert self.options['re_record_interval'] == 10000
        assert self.options['match_requests_on'] == ['method']

        data = self.data.copy()
        data['match_requests_on'] = ['foo', 'bar', 'bogus']
        options = Options(data)
        assert options['match_requests_on'] == ['method', 'uri']
