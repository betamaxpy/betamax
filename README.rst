betamax
=======

A VCR_-like adapter for requests. This will make mocking out requests much
easier.

Example Use
-----------

.. code::

    from betamax import VCR
    from requests import Session
    from unittest import TestCase

    VCR.cassette_library_dir = 'tests/fixtures/cassettes'


    class TestGitHubAPI(TestCase):
        def setUp(self):
            self.session = Session()
            self.headers.update(...)

        # Set the cassette in a line other than the context declaration
        def test_user(self):
            with VCR(self.session) as vcr:
                vcr.use_cassette('user')
                resp = self.session.get('https://api.github.com/user',
                                        auth=('user', 'pass'))
                assert resp.json()['login'] is not None

        # Set the cassette in line with the context declaration
        def test_repo(self):
            with VCR(self.session).use_cassette('repo') as vcr:
                resp = self.session.get(
                    'https://api.github.com/repos/sigmavirus24/github3.py'
                    )
                assert resp.json()['owner'] != {}

VCR Cassette Compatiblity
-------------------------

There are some differences in how betamax and VCR_ record cassettes. It seems
unlikely that someone will want to use the same cassettes in both python and
ruby but if the demand is great enough, the inconsistencies can be fixed.

.. _VCR: https://github.com/vcr/vcr
