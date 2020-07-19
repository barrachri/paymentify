from functools import wraps
from types import MappingProxyType

import falcon
import stripe

# Matching https://stripe.com/docs/api/errors
STRIPE_HTTP_STATUS_ERROR = MappingProxyType(
    {
        400: falcon.HTTP_400,
        401: falcon.HTTP_401,
        402: falcon.HTTP_402,
        403: falcon.HTTP_403,
        404: falcon.HTTP_404,
        409: falcon.HTTP_409,
        500: falcon.HTTP_500,
        502: falcon.HTTP_502,
        503: falcon.HTTP_503,
        504: falcon.HTTP_504,
    }
)


def stripe_catcher(func):
    """Catch Stripe exception and return a valid error response"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except stripe.error.StripeError as e:
            # use 400 as default
            http_status_code = STRIPE_HTTP_STATUS_ERROR.get(
                e.http_status, falcon.HTTP_400
            )
            result = (
                {"type": e.error.type, "message": e.error.message},
                http_status_code,
            )
        return result

    return wrapper
