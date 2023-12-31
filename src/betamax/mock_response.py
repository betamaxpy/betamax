# noqa: D100
from email import parser, message
import sys


class MockHTTPResponse(object):  # noqa: D101
    def __init__(self, headers):  # noqa: D107
        from betamax.util import coerce_content

        h = ["%s: %s" % (k, v) for k in headers for v in headers.getlist(k)]
        h = map(coerce_content, h)
        h = '\r\n'.join(h)
        if sys.version_info < (2, 7):
            h = h.encode()
        p = parser.Parser(EmailMessage)
        # Thanks to Python 3, we have to use the slightly more awful API below
        # mimetools was deprecated so we have to use email.message.Message
        # which takes no arguments in its initializer.
        self.msg = p.parsestr(h)
        self.msg.set_payload(h)

    def isclosed(self):  # noqa: D102
        return False


class EmailMessage(message.Message):  # noqa: D101
    def getheaders(self, value, *args):  # noqa: D102
        return self.get_all(value, [])
