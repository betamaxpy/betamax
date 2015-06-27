import betamax
from betamax_serializers import pretty_json
import requests

CASSETTE_LIBRARY_DIR = 'examples/cassettes/'


def main():
    session = requests.Session()
    betamax.Betamax.register_serializer(pretty_json.PrettyJSONSerializer)
    recorder = betamax.Betamax(
        session, cassette_library_dir=CASSETTE_LIBRARY_DIR
    )
    matchers = ['method', 'uri', 'body']

    with recorder.use_cassette('more-complicated-cassettes',
                               serialize_with='prettyjson',
                               match_requests_on=matchers):
        session.get('https://httpbin.org/get')
        session.post('https://httpbin.org/post',
                     params={'id': '20'},
                     json={'some-attribute': 'some-value'})
        session.get('https://httpbin.org/get', params={'id': '20'})
        session.post('https://httpbin.org/post',
                     params={'id': '20'},
                     json={'some-other-attribute': 'some-other-value'})


if __name__ == '__main__':
    main()
