from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import dotenv_values
import os

# class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
#
#     def do_GET(self):
#         config_env = {
#             **dotenv_values(".env"),
#             **os.environ
#         }
#         self.send_response(200)
#         self.end_headers()
#         print(os.environ['APP_ENV'])
#         arr = bytes(config_env["PASSWORD"], 'utf-8')
#         self.wfile.write(arr)
#
#
# httpd = HTTPServer(('localhost', 3246), SimpleHTTPRequestHandler)
# httpd.serve_forever()

#!/usr/bin/env python3
#
import datetime
import socket
import sys

# Block size is set to 8192 because thats usually the max header size
BLOCK_SIZE = 8192

def serve(host='127.0.0.1', port=3246, verbosity=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(1)

        if verbosity > 0:
            print('Echoing')

        while True:
            connection, client_address = sock.accept()

            request = {}
            bytes_left = BLOCK_SIZE
            while bytes_left > 0:
                if bytes_left > BLOCK_SIZE:
                    data = connection.recv(BLOCK_SIZE)
                else:
                    data = connection.recv(max(0, bytes_left))

                if not 'header' in request:
                    request = build_request(data)
                    header_length = len(request['raw']) - len(request['body'])
                    body_length_read = BLOCK_SIZE - header_length
                    if 'content-length' in request['header']:
                        bytes_left = int(request['header']['content-length']) - body_length_read
                    else:
                        bytes_left = 0
                else:
                    request['raw'] += data
                    request['body'] += data.decode('utf-8', 'ignore')
                    bytes_left -= BLOCK_SIZE

            request_time = datetime.datetime.now().ctime()

            if verbosity > 0:
                print(' - '.join([client_address[0], request_time, request['header']['request-line']]))

            raw_decoded = request['raw'].decode('utf-8', 'ignore')
            response = "HTTP/1.1 200 OK\nAccess-Control-Allow-Origin: *\n\n{}".format(raw_decoded)
            if verbosity == 2:
                print("-"*10)
                print(response)
                print("-"*40)
            connection.sendall(response.encode())
            connection.close()
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        sock.close()


def build_request(first_chunk):
    lines = first_chunk.decode('utf-8', 'ignore').split('\r\n')
    h = {'request-line': lines[0]}
    i = 1
    while i < len(lines[1:]) and lines[i] != '':
        k, v = lines[i].split(': ')
        h.update({k.lower(): v})
        i += 1
    r = {
        "header": h,
        "raw": first_chunk,
        "body": lines[-1]
    }
    return r


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Server that returns any http request made to it")
    parser.add_argument('-b', '--bind', default='localhost', help='host to bind to')
    parser.add_argument('-p', '--port', default=3246, type=int, help='port to listen on')
    parser.add_argument('-v', '--verbose', action='store_true', help='print all requests to terminal')
    parser.add_argument('-q', '--quiet', action='store_true', help='silence all output (overrides --verbose)')
    args = parser.parse_args()
    host = args.bind
    port = args.port
    verbose = args.verbose
    quiet = args.quiet

    verbosity = 1
    if verbose:
        verbosity = 2
    if quiet:
        verbosity = 0

    serve(host, port, verbosity)
