# python-http-server

An HTTP server in Python, written with only the standard library. It serves
files statically from a directory and its subdirectories (by default
`(working directory)/public`).

# Quick start
1. Clone the repository or use another method to obtain the project
    ```sh
    git clone https://github.com/dangduomg/python-http-server
    ```
2. Navigate to the project root
    ```sh
    cd python-http-server
    ```
3. Run `server.py`. It's already executable
    ```
    ./server.py
    ```
4. Open `localhost:8000` on the browser
5. Done!

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