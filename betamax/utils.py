import io
from requests.compat import is_py2


def coerce_content(content, encoding):
    if hasattr(content, 'decode') and not is_py2:
        return content.decode(encoding) if encoding else content.decode()
    return content


def body_io(string, encoding):
    if is_py2:
        return io.StringIO(string)
    if hasattr(string, 'encode'):
        string = string.encode(encoding)
    return io.BytesIO(string)
