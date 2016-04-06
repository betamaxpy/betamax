from betamax import Betamax, BetamaxError

from tests.integration.helper import IntegrationHelper


class TestRecordOnce(IntegrationHelper):
    def test_records_new_interaction(self):
        s = self.session
        with Betamax(s).use_cassette('test_record_once') as betamax:
            self.cassette_path = betamax.current_cassette.cassette_path
            assert betamax.current_cassette.is_empty() is True
            r = s.get('http://httpbin.org/get')
            assert r.status_code == 200
            assert betamax.current_cassette.is_empty() is True
            assert betamax.current_cassette.interactions != []

    def test_replays_response_from_cassette(self):
        s = self.session
        with Betamax(s).use_cassette('test_replays_response') as betamax:
            self.cassette_path = betamax.current_cassette.cassette_path
            assert betamax.current_cassette.is_empty() is True
            r0 = s.get('http://httpbin.org/get')
            assert r0.status_code == 200
            assert betamax.current_cassette.interactions != []
            assert len(betamax.current_cassette.interactions) == 1
            r1 = s.get('http://httpbin.org/get')
            assert len(betamax.current_cassette.interactions) == 2
            assert r1.status_code == 200
            assert r0.headers == r1.headers
            assert r0.content == r1.content


class TestRecordNone(IntegrationHelper):
    def test_raises_exception_when_no_interactions_present(self):
        s = self.session
        with Betamax(s) as betamax:
            betamax.use_cassette('test', record='none')
            self.cassette_created = False
            assert betamax.current_cassette is not None
            self.assertRaises(BetamaxError, s.get, 'http://httpbin.org/get')

    def test_record_none_does_not_create_cassettes(self):
        s = self.session
        with Betamax(s) as betamax:
            self.assertRaises(ValueError, betamax.use_cassette,
                              'test_record_none', record='none')
        self.cassette_created = False


class TestRecordNewEpisodes(IntegrationHelper):
    def setUp(self):
        super(TestRecordNewEpisodes, self).setUp()
        with Betamax(self.session).use_cassette('test_record_new'):
            self.session.get('http://httpbin.org/get')
            self.session.get('http://httpbin.org/redirect/2')

    def test_records_new_events_with_existing_cassette(self):
        s = self.session
        opts = {'record': 'new_episodes'}
        with Betamax(s).use_cassette('test_record_new', **opts) as betamax:
            cassette = betamax.current_cassette
            self.cassette_path = cassette.cassette_path
            assert cassette.interactions != []
            assert len(cassette.interactions) == 4
            assert cassette.is_empty() is False
            s.get('https://httpbin.org/get')
            assert len(cassette.interactions) == 5

        with Betamax(s).use_cassette('test_record_new') as betamax:
            cassette = betamax.current_cassette
            assert len(cassette.interactions) == 5
            r = s.get('https://httpbin.org/get')
            assert r.status_code == 200


class TestRecordNewEpisodesCreatesCassettes(IntegrationHelper):
    def test_creates_new_cassettes(self):
        recorder = Betamax(self.session)
        opts = {'record': 'new_episodes'}
        cassette_name = 'test_record_new_makes_new_cassettes'
        with recorder.use_cassette(cassette_name, **opts) as betamax:
            self.cassette_path = betamax.current_cassette.cassette_path
            self.session.get('https://httpbin.org/get')


class TestRecordAll(IntegrationHelper):
    def setUp(self):
        super(TestRecordAll, self).setUp()
        with Betamax(self.session).use_cassette('test_record_all'):
            self.session.get('http://httpbin.org/get')
            self.session.get('http://httpbin.org/redirect/2')

    def test_records_new_interactions(self):
        s = self.session
        opts = {'record': 'all'}
        with Betamax(s).use_cassette('test_record_all', **opts) as betamax:
            cassette = betamax.current_cassette
            self.cassette_path = cassette.cassette_path
            assert cassette.interactions != []
            assert len(cassette.interactions) == 4
            assert cassette.is_empty() is False
            s.post('http://httpbin.org/post', data={'foo': 'bar'})
            assert len(cassette.interactions) == 5

        with Betamax(s).use_cassette('test_record_all') as betamax:
            assert len(betamax.current_cassette.interactions) == 5
