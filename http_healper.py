
HTTP_OK = b"""\
HTTP/1.1 200 OK

"""

HTTP_Unauthorized = b"""\
HTTP/1.1 401 Unauthorized

{'result': false, 'error': 401}
"""

HTTP_Not_Found = b"""\
HTTP/1.1 404 Not Found

{'result': false, 'error': 404}
"""


def http_response(res):
    return HTTP_OK + bytes(res, 'utf-8')
