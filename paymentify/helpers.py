from functools import wraps

import stripe


def stripe_catcher(func):
    """Catch Stripe expection and return a valid error response"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except stripe.error.StripeError as e:
            result = (
                {"type": "processor_error", "message": e.error.message},
                str(e.http_status),
            )
        return result

    return wrapper
