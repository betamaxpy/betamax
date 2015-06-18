import functools

import requests

from . import recorder


def use_cassette(cassette_name, cassette_library_dir=None,
                 default_cassette_options={}, **use_cassette_kwargs):
    """Decorator that provides a Betamax-wrapped Session for tests."""
    def actual_decorator(func):
        @functools.wraps(func)
        def test_wrapper(*args, **kwargs):
            session = requests.Session()
            recr = recorder.Betamax(
                session=session,
                cassette_library_dir=cassette_library_dir,
                default_cassette_options=default_cassette_options
            )
            with recr.use_cassette(cassette_name, **use_cassette_kwargs):
                func(session, *args, **kwargs)

        return test_wrapper
    return actual_decorator
