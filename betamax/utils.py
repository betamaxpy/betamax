import io
from requests.compat import is_py2


def coerce_content(content, encoding):
    if hasattr(content, 'decode') and not is_py2:
        if encoding:
            content = content.decode(encoding)
        else:
            content = content.decode()
    return content


def body_io(string, encoding):
    if is_py2:
        return io.StringIO(string)
    if hasattr(string, 'encode'):
        if encoding:
            string = string.encode(encoding)
        else:
            string = string.encode()
    return io.BytesIO(string)
