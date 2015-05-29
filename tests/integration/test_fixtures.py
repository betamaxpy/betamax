import os.path

import pytest


@pytest.mark.usefixtures('betamax_session')
class TestPyTestFixtures:
    @pytest.fixture(autouse=True)
    def setup(self, request):
        """After test hook to assert everything."""
        def finalizer():
            test_dir = os.path.abspath('.')
            cassette_name = ('tests.integration.test_fixtures.'  # Module name
                             'TestPyTestFixtures.'  # Class name
                             'test_pytest_fixture'  # Test function name
                             '.json')
            file_name = os.path.join(test_dir, 'tests', 'cassettes',
                                     cassette_name)
            assert os.path.exists(file_name) is True

        request.addfinalizer(finalizer)

    def test_pytest_fixture(self, betamax_session):
        """Exercise the fixture itself."""
        resp = betamax_session.get('https://httpbin.org/get')
        assert resp.ok
