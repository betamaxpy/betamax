betamax
=======

A VCR_-like adapter for requests. This will make mocking out requests much
easier. Tested on `Travis CI`_.

Example Use
-----------

.. code::

    from betamax import Betamax
    from requests import Session
    from unittest import TestCase

    with Betamax.configure() as config:
        config.cassette_library_dir = 'tests/fixtures/cassettes'


    class TestGitHubAPI(TestCase):
        def setUp(self):
            self.session = Session()
            self.headers.update(...)

        # Set the cassette in a line other than the context declaration
        def test_user(self):
            with Betamax(self.session) as vcr:
                vcr.use_cassette('user')
                resp = self.session.get('https://api.github.com/user',
                                        auth=('user', 'pass'))
                assert resp.json()['login'] is not None

        # Set the cassette in line with the context declaration
        def test_repo(self):
            with Betamax(self.session).use_cassette('repo') as vcr:
                resp = self.session.get(
                    'https://api.github.com/repos/sigmavirus24/github3.py'
                    )
                assert resp.json()['owner'] != {}

VCR Cassette Compatiblity
-------------------------

Betamax can use any VCR-recorded cassette as of this point in time. The only
caveat is that python-requests returns a URL on each response. VCR does not
store that in a cassette now but we will. Any VCR-recorded cassette used to
playback a response will unfortunately not have a URL attribute on responses
that are returned. This is a minor annoyance but not something that can be
fixed.

.. _VCR: https://github.com/vcr/vcr
.. _Travis CI: https://travis-ci.org/sigmavirus24/betamax
