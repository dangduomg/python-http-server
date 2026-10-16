#!/usr/bin/env python3
"""i made a basic http handler"""

import argparse
from http.server import HTTPServer
from pathlib import Path

from file_handler import FileServerReqHandler

# argument parser object
argparser = argparse.ArgumentParser(
    prog='server.py',
    description="""\
a simple http server that serves files from a directory and its subdirectories.
""",
)
argparser.add_argument(
    '--base-path',
    type=str,
    default='./public',
    help="""\
the base path to serve files from (default: ./public)
""",
)
argparser.add_argument(
    '--index-files',
    type=str,
    nargs='*',
    default=['index.html', 'index.htm'],
    help="""\
the index files to look for in directories (default: index.html index.htm)
""",
)
argparser.add_argument(
    '--host',
    type=str,
    default='localhost',
    help='the host to bind the server to (default: localhost)',
)
argparser.add_argument(
    '--port',
    type=int,
    default=8000,
    help='the port to bind the server to (default: 8000)',
)


def main():
    """main function"""
    args = argparser.parse_args()
    try:
        FileServerReqHandler.base_path = (
            Path(args.base_path).resolve(strict=True)
        )
    except FileNotFoundError:
        print(f'base path {args.base_path} does not exist')
        return
    FileServerReqHandler.index_files = args.index_files
    server = HTTPServer((args.host, args.port), FileServerReqHandler)

    print('minimal http server')
    print("don't use in production")
    print(f'server now starts to serve at {args.host}:{args.port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print('server closed')


if __name__ == '__main__':
    main()
