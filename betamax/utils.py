import io
from requests.compat import is_py2


def coerce_content(content, encoding):
    if encoding:
        content = content.decode(encoding, errors='replace')
    else:
        content = content.decode(errors='replace')
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
