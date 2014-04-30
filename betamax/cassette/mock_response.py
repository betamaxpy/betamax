import io
import email.message


class MockHTTPResponse(object):
    def __init__(self, headers):
        from .util import coerce_content

        h = ["%s: %s" % (k, v) for (k, v) in headers.items()]
        h = map(coerce_content, h)
        h = io.StringIO('\r\n'.join(h) or None)
        # Thanks to Python 3, we have to use the slightly more awful API below
        # mimetools was deprecated so we have to use email.message.Message
        # which takes no arguments in its initializer.
        self.msg = EmailMessage()
        self.msg.set_payload(h)

    def isclosed(self):
        return False


class EmailMessage(email.message.Message):
    def getheaders(self, value, *args):
        return self.get(value, *args)
