import os
import sys
import betamax

sys.path.insert(0, os.path.abspath('.'))

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = 'tests/cassettes/'
