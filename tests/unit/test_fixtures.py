try:
    import unittest.mock as mock
except ImportError:
    import mock

import unittest

import betamax
from betamax.fixtures import pytest as pytest_fixture


class TestPyTestFixture(unittest.TestCase):
    def setUp(self):
        self.mocked_betamax = mock.MagicMock()
        self.patched_betamax = mock.patch.object(
            betamax.recorder, 'Betamax', return_value=self.mocked_betamax)
        self.patched_betamax.start()

    def tearDown(self):
        self.patched_betamax.stop()

    def test_adds_stop_as_a_finalizer(self):
        # Mock a pytest request object
        request = mock.MagicMock()
        request.cls = request.module = None
        request.function.__name__ = 'test'

        pytest_fixture.betamax_session(request)
        assert request.addfinalizer.called is True
        request.addfinalizer.assert_called_once_with(self.mocked_betamax.stop)

    def test_auto_starts_the_recorder(self):
        # Mock a pytest request object
        request = mock.MagicMock()
        request.cls = request.module = None
        request.function.__name__ = 'test'

        pytest_fixture.betamax_session(request)
        self.mocked_betamax.start.assert_called_once_with()
