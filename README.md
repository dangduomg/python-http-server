# python-http-server

An HTTP server in Python. It serves files statically from a directory and its
subdirectories (by default `(working directory)/public`).

# Usage
```
usage: server.py [-h] [--base-path BASE_PATH] [--index-files [INDEX_FILES ...]] [--host HOST] [--port PORT]

a simple http server that serves files from a directory and its subdirectories.

options:
  -h, --help            show this help message and exit
  --base-path BASE_PATH
                        the base path to serve files from (default: ./public)
  --index-files [INDEX_FILES ...]
                        the index files to look for in directories (default: index.html index.htm)
  --host HOST           the host to bind the server to (default: localhost)
  --port PORT           the port to bind the server to (default: 8000)
```