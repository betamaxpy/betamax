import unittest

import requests

from .. import recorder


class BetamaxTestCase(unittest.TestCase):
    def _generate_cassette_name(self):
        cls = self.__class_.__name__
        test = self._testMethodName
        return '{0}.{1}'.format(cls, test)

    def setUp(self):
        super(BetamaxTestCase, self).setUp()

        cassette_name = self._generate_cassette_name()

        self.sesion = requests.Session()
        self.recorder = recorder.Betamax(session=self.session)
        self.recorder.use_cassette(cassette_name)
        self.recorder.start()

    def tearDown(self):
        super(BetamaxTestCase, self).tearDown()
        self.recorder.stop()
