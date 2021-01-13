
HTTP_OK = b"HTTP/1.0 200 OK\r\nContent-type: application/json; charset=utf-8\r\n\r\n"

HTTP_Unauthorized = b"HTTP/1.1 401 Unauthorized\r\nContent-type: application/json; charset=utf-8\r\n\r\n{'result': false, 'error': 401}"

HTTP_Not_Found = b"HTTP/1.1 404 Not Found\r\nContent-type: application/json; charset=utf-8\r\n\r\n{'result': false, 'error': 404}"


def http_response(res):
    return HTTP_OK + bytes(res, 'utf-8')
