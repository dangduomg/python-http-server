"""errors"""


class RequestError(Exception):
    """base class for request errors"""


class NotFoundError(RequestError):
    """raises when a resource is not found

    expected error code: 404
    """


class ForbiddenError(RequestError):
    """raises when a resource is forbidden

    expected error code: 403
    """
