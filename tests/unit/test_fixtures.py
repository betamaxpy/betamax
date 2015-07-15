try:
    import unittest.mock as mock
except ImportError:
    import mock

import pytest
import unittest

import requests

import betamax
from betamax.fixtures import pytest as pytest_fixture
from betamax.fixtures import unittest as unittest_fixture


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


class TestUnittestFixture(unittest.TestCase):
    def setUp(self):
        self.mocked_betamax = mock.MagicMock()
        self.patched_betamax = mock.patch.object(
            betamax.recorder, 'Betamax', return_value=self.mocked_betamax)
        self.betamax = self.patched_betamax.start()
        self.fixture = unittest_fixture.BetamaxTestCase()

    def tearDown(self):
        self.patched_betamax.stop()

    def test_generate_cassete_name(self):
        test_method = mock.MagicMock()
        test_method.__class__.__name__ = 'Testing123'
        test_method._testMethodName = 'test_method_name'

        name = unittest_fixture.BetamaxTestCase.generate_cassette_name(
            test_method)
        assert name == 'Testing123.test_method_name'

    def test_setUp(self):
        self.fixture.setUp()

        self.mocked_betamax.use_cassette.assert_called_once_with(
            'BetamaxTestCase.runTest'
        )
        self.mocked_betamax.start.assert_called_once_with()

    def test_setUp_rejects_arbitrary_session_classes(self):
        self.fixture.SESSION_CLASS = object

        with pytest.raises(AssertionError):
            self.fixture.setUp()

    def test_setUp_accepts_session_subclasses(self):
        class TestSession(requests.Session):
            pass

        self.fixture.SESSION_CLASS = TestSession

        self.fixture.setUp()

        assert self.betamax.called is True
        call_kwargs = self.betamax.call_args[-1]
        assert isinstance(call_kwargs['session'], TestSession)

    def test_tearDown_calls_stop(self):
        recorder = mock.Mock()
        self.fixture.recorder = recorder

        self.fixture.tearDown()

        recorder.stop.assert_called_once_with()
