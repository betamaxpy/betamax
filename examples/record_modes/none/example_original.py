import betamax
import requests

CASSETTE_LIBRARY_DIR = 'examples/record_modes/none/'


def main():
    session = requests.Session()
    recorder = betamax.Betamax(
        session, cassette_library_dir=CASSETTE_LIBRARY_DIR
    )

    with recorder.use_cassette('none-example', record='none'):
        session.get('https://httpbin.org/get')
        session.post('https://httpbin.org/post',
                     params={'id': '20'},
                     json={'some-attribute': 'some-value'})
        session.get('https://httpbin.org/get', params={'id': '20'})


if __name__ == '__main__':
    main()
