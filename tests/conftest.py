import os
import sys
import betamax

sys.path.insert(0, os.path.abspath('.'))

betamax.Betamax.cassette_library_dir = 'tests/cassettes/'
