import sys

from betamax import Betamax

from .helper import IntegrationHelper


class TestRequestHeaders(IntegrationHelper):

    def test_response_request_header_types(self):
        bytestring = b'bytes' if sys.version_info[0] > 2 else 'bytes'
        textstring = 'str' if sys.version_info[0] > 2 else u'str'
        headers = {'ByteHeader': bytestring, 'TextHeader': textstring}
        url = 'http://httpbin.org/'

        recorder = Betamax(self.session)
        cassette_name = 'test-response-request-header-types'
        self.cassette_path = cassette_name

        # serialize_with = 'json'
        serialize_with = 'pickle'

        with recorder.use_cassette(cassette_name, serialize_with=serialize_with) as r:
            self.cassette_path = r.current_cassette.cassette_path
            response_record = self.session.get(url, headers=headers)

        with recorder.use_cassette(cassette_name, serialize_with=serialize_with):
            response_playback = self.session.get(url, headers=headers)

        bytes_record = response_record.request.headers['ByteHeader']
        bytes_playback = response_playback.request.headers['ByteHeader']

        text_record = response_record.request.headers['TextHeader']
        text_playback = response_playback.request.headers['TextHeader']

        self.assertEqual(type(bytes_record), type(bytes_playback))
        self.assertEqual(type(text_record), type(text_playback))

        if sys.version_info[0] > 2:
            self.assertEqual(bytes_playback, b'bytes')
            self.assertEqual(text_playback, 'str')
        else:
            self.assertTrue(isinstance(bytes_playback, str))
            self.assertEqual(bytes_playback, 'bytes')
            self.assertTrue(isinstance(text_playback, unicode))
            self.assertEqual(text_playback, 'str')
