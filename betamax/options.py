#from betamax.cassette import Cassette
from betamax.new_cassette import NewCassette


def validate_record(record):
    return record in ['all', 'new_episodes', 'none', 'once']


def validate_matchers(matchers):
    from betamax.matchers import matcher_registry
    available_matchers = list(matcher_registry.keys())
    return all(m in available_matchers for m in matchers)


def translate_cassette_options():
    for (k, v) in NewCassette.default_cassette_options.items():
        yield (k, v) if k != 'record_mode' else ('record', v)


class Options(object):
    valid_options = {
        'match_requests_on': validate_matchers,
        're_record_interval': lambda x: x is None or x > 0,
        'record': validate_record,
        'serialize': lambda x: x in ['json'],
    }

    defaults = {
        'match_requests_on': ['method', 'uri'],
        're_record_interval': None,
        'record': 'once',
        'serialize': 'json',
    }

    def __init__(self, data=None):
        self.data = data or {}
        self.validate()
        self.defaults = Options.defaults.copy()
        self.defaults.update(translate_cassette_options())

    def __repr__(self):
        return 'Options(%s)' % self.data

    def __getitem__(self, key):
        return self.data.get(key, self.defaults.get(key))

    def __setitem__(self, key, value):
        self.data[key] = value
        return value

    def __delitem__(self, key):
        del self.data[key]

    def __contains__(self, key):
        return key in self.data

    def items(self):
        return self.data.items()

    def validate(self):
        for key, value in list(self.data.items()):
            if key not in Options.valid_options:
                del self[key]
            else:
                is_valid = Options.valid_options[key]
                if not is_valid(value):
                    del self[key]
