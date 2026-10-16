"""routed GET method handler"""


import re
from collections.abc import Callable
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlsplit

from errors import ForbiddenError, NotFoundError

type DispatchResult = tuple[dict[str, str], bytes]
type DispatchCallback = Callable[
    ['RoutedGetHandler', 'Arguments'], DispatchResult
]


@dataclass(frozen=True)
class Arguments:
    """arguments extracted from url"""
    path: re.Match
    query: dict

    @classmethod
    def from_url(cls, route_pat: str, url: str) -> 'Arguments | None':
        """extract arguments from url"""
        split = urlsplit(url)
        path = re.fullmatch(route_pat, split.path)
        if not path:
            return None
        query = parse_qs(split.query)
        return cls(path, query)


@dataclass(frozen=True)
class Dispatch:
    """a dispatch for a route

    it accepts two arguments: the handler object and the Arguments object
    """

    route_pat: str
    callback: DispatchCallback

    def __call__(
        self, handler: 'RoutedGetHandler', args: Arguments
    ) -> DispatchResult:
        """dispatch the request to the callback"""
        return self.callback(handler, args)


class RoutedGetHandler(BaseHTTPRequestHandler):
    """routed GET method handler"""

    def do_GET(self) -> None:
        """handle GET method"""
        # pylint: disable=invalid-name
        try:
            # try routes
            # search among Dispatch objects in the class
            for dispatch in type(self).__dict__.values():
                if isinstance(dispatch, Dispatch):
                    args = Arguments.from_url(dispatch.route_pat, self.path)
                    if args is not None:
                        headers, response_content = dispatch(self, args)
                        self._send_succ_response(headers, response_content)
                        return
            raise NotFoundError
        except ForbiddenError:
            self.send_error(403)
            return
        except NotFoundError:
            self.send_error(404)
            return
        except Exception:
            self.send_error(500)
            raise

    def _send_succ_response(
        self, headers: dict[str, str], response_content: bytes
    ) -> None:
        """send a successful response

        from this point, no errors will result in an error response
        """
        self.send_response(200)
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(response_content)

    @staticmethod
    def dispatch(route_pat: str):
        """transform a callback method into a dispatch"""
        return lambda callback: Dispatch(route_pat, callback)
