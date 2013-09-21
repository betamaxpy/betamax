import io


def coerce_content(content, encoding=None):
    if hasattr(content, 'decode'):
        content = content.decode(encoding or 'utf-8', 'replace')
    return content


def body_io(string, encoding=None):
    if hasattr(string, 'encode'):
        string = string.encode(encoding or 'utf-8')
    return io.BytesIO(string)
