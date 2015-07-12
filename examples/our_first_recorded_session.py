import betamax
import requests

CASSETTE_LIBRARY_DIR = 'examples/cassettes/'


def main():
    session = requests.Session()
    recorder = betamax.Betamax(
        session, cassette_library_dir=CASSETTE_LIBRARY_DIR
    )

    with recorder.use_cassette('our-first-recorded-session'):
        session.get('https://httpbin.org/get')


if __name__ == '__main__':
    main()
