import betamax
import requests

CASSETTE_LIBRARY_DIR = 'examples/record_modes/once/'


def main():
    session = requests.Session()
    recorder = betamax.Betamax(
        session, cassette_library_dir=CASSETTE_LIBRARY_DIR
    )

    with recorder.use_cassette('once-example', record='once'):
        session.get('https://httpbin.org/get')
        session.post('https://httpbin.org/post',
                     params={'id': '20'},
                     json={'some-attribute': 'some-value'})
        session.get('https://httpbin.org/get', params={'id': '20'})
        session.get('https://httpbin.org/get', params={'id': '40'})


if __name__ == '__main__':
    main()
