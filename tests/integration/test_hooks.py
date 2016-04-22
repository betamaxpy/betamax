import betamax

from . import helper


def prerecord_hook(interaction, cassette):
    assert cassette.interactions == []
    interaction.data['response']['headers']['Betamax-Fake-Header'] = 'success'


def ignoring_hook(interaction, cassette):
    interaction.ignore()


def preplayback_hook(interaction, cassette):
    assert cassette.interactions != []
    interaction.data['response']['headers']['Betamax-Fake-Header'] = 'temp'


class TestHooks(helper.IntegrationHelper):
    def tearDown(self):
        super(TestHooks, self).tearDown()
        # Clear out the hooks
        betamax.cassette.Cassette.hooks.pop('before_record', None)
        betamax.cassette.Cassette.hooks.pop('before_playback', None)

    def test_prerecord_hook(self):
        with betamax.Betamax.configure() as config:
            config.before_record(callback=prerecord_hook)

        recorder = betamax.Betamax(self.session)
        with recorder.use_cassette('prerecord_hook'):
            self.cassette_path = recorder.current_cassette.cassette_path
            response = self.session.get('https://httpbin.org/get')
            assert response.headers['Betamax-Fake-Header'] == 'success'

        with recorder.use_cassette('prerecord_hook', record='none'):
            response = self.session.get('https://httpbin.org/get')
            assert response.headers['Betamax-Fake-Header'] == 'success'

    def test_preplayback_hook(self):
        with betamax.Betamax.configure() as config:
            config.before_playback(callback=preplayback_hook)

        recorder = betamax.Betamax(self.session)
        with recorder.use_cassette('preplayback_hook'):
            self.cassette_path = recorder.current_cassette.cassette_path
            self.session.get('https://httpbin.org/get')

        with recorder.use_cassette('preplayback_hook', record='none'):
            response = self.session.get('https://httpbin.org/get')
            assert response.headers['Betamax-Fake-Header'] == 'temp'

    def test_prerecord_ignoring_hook(self):
        with betamax.Betamax.configure() as config:
            config.before_record(callback=ignoring_hook)

        recorder = betamax.Betamax(self.session)
        with recorder.use_cassette('ignore_hook'):
            self.cassette_path = recorder.current_cassette.cassette_path
            self.session.get('https://httpbin.org/get')
            assert recorder.current_cassette.interactions == []
