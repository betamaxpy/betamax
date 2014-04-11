from .helper import IntegrationHelper
from betamax import Betamax


class TestPreserveExactBodyBytes(IntegrationHelper):
    def test_preserve_exact_body_bytes_does_not_munge_response_content(self):
        # Do not delete this cassette after the test
        self.cassette_created = False

        with Betamax(self.session) as b:
            b.use_cassette('preserve_exact_bytes',
                           preserve_exact_body_bytes=True)
            r = self.session.get('https://httpbin.org/get')
            assert 'headers' in r.json()
