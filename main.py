try:
    import usocket as socket
except:
    import socket

from led import Led
from esp_manager import Esp
from http_healper import http_response, HTTP_Not_Found, HTTP_Unauthorized

led = Led()
esp = Esp()

Data = None
Authed = False
Key = bytes('12345', 'utf-8')


def serve_response(method, route, data):
    if method == b'POST':

        if route == b'/init':
            esp.db_init()
            esp.ap_init()
            esp.sta_init()
            res = '{"result": true}'

        elif route == b'/vars':
            res = led.set_vars(data)

        elif route == b'/ap_change_password':
            res = esp.ap_change_password(data)

        elif route == b'/sta_connect':
            res = esp.sta_connect(data)

        elif route == b'/sta_active':
            res = esp.sta_active()

        elif route == b'/sta_deactive':
            res = esp.sta_deactive()

        else:
            return HTTP_Not_Found

        return http_response(res)

    elif method == b'GET':

        if route == b'/vars':
            res = led.get_vars()

        elif route == b'/sta_scan':
            res = esp.sta_scan()

        elif route == b'/sta_isconnected':
            res = esp.sta_isconnected()

        else:
            return HTTP_Not_Found

        return http_response(res)

    return HTTP_Not_Found


def check_request(str):
    method, route, ver = False, False, False
    try:
        method, route, ver = str.split(None, 3)
        if method not in [b'POST', b'GET']:
            method = False
    except Exception as e:
        print('error', e)
        raise
    finally:
        return method, route, ver


def parse_header(str):
    global Data, Authed, Key
    h = [i.strip() for i in str.split(b':', 1)]
    if h[0] == b'data':
        Data = h[1]
    if h[0] == b'key':
        Authed = h[1] == Key


async def start(micropython_optimize=False):
    global Authed
    s = socket.socket()

    # Binding to all interfaces - server will be accessible to other hosts!
    ai = socket.getaddrinfo("0.0.0.0", 8585)
    print("Bind address info:", ai)
    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://<this_host>:8585/")

    while True:
        client_sock, client_addr = s.accept()

        print("Client address:", client_addr)
        print("Client socket:", client_sock)

        if not micropython_optimize:
            # To read line-oriented protocol (like HTTP) from a socket (and
            # avoid short read problem), it must be wrapped in a stream (aka
            # file-like) object. That's how you do it in CPython:
            client_stream = client_sock.makefile("rwb")
        else:
            # .. but MicroPython socket objects support stream interface
            # directly, so calling .makefile() method is not required. If
            # you develop application which will run only on MicroPython,
            # especially on a resource-constrained embedded device, you
            # may take this shortcut to save resources.
            client_stream = client_sock

        # print("Request:")
        h = client_stream.readline()
        method, route, ver = check_request(h)
        # print(h)
        while True:
            h = client_stream.readline()
            parse_header(h)
            if h == b"" or h == b"\r\n":
                break
            # print(h)

        print("Parsed:", method, route, ver, Authed)

        if Authed:
            res = serve_response(method, route, Data)
            client_stream.write(res)
        else:
            client_stream.write(HTTP_Unauthorized)

        Authed = False
        # client_sock.sendall(CONTENT )
        client_stream.close()
        if not micropython_optimize:
            client_sock.close()
