"""a simple http request handler

serve files from the working directory and its subdirectories"""

import mimetypes
from pathlib import Path

from errors import ForbiddenError, NotFoundError
from route import Arguments, DispatchResult, RoutedGetHandler


class FileServerReqHandler(RoutedGetHandler):
    """a simple http request handler

    serve files from the working directory and its subdirectories
    """

    base_path: Path
    index_files: list[str]

    @RoutedGetHandler.dispatch(r'/.*')
    def handle_route(self, args: Arguments) -> DispatchResult:
        """handle the route"""
        # resolve the path
        resolved_path = self.resolve_path(args.path[0])

        # prepare headers
        mime_type, _ = mimetypes.guess_type(resolved_path)
        headers = {
            'Content-Type': (
                'application/octet-stream' if mime_type is None else mime_type
            ),
        }

        # fetch the content
        try:
            with resolved_path.open('rb') as f:
                response_content = f.read()
        except PermissionError as e:
            raise ForbiddenError from e

        return headers, response_content

    def resolve_path(self, path):
        """resolve a path relative to the base path"""
        # first immediately resolve the path
        res = self._resolve_path(self.base_path / path.lstrip('/'))

        # special handling if path is a directory
        if res.is_dir():
            for fname in self.index_files:
                index_path = res / fname
                try:
                    candidate = self._resolve_path(index_path)
                except NotFoundError:
                    continue
                if candidate.is_file():
                    res = candidate
                    break
            else:
                raise ForbiddenError

        # finally, res must be a file
        if not res.is_file():
            raise ForbiddenError

        return res

    def _resolve_path(self, path):
        """resolve the immediate path (no special handling for directories)"""
        # check if the path is valid and resolve
        try:
            res = path.resolve(strict=True)
        except FileNotFoundError as e:
            raise NotFoundError from e
        except NotADirectoryError as e:
            raise NotFoundError from e

        # ensure path is within base
        if not res.is_relative_to(self.base_path):
            raise ForbiddenError

        return res
