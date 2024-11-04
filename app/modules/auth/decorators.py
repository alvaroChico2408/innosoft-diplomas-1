from flask_login import current_user
from core.decorators.decorators import pass_or_abort
from functools import wraps
from flask import flash, redirect, request, url_for


def guest_required(f):

    def condition(**kwargs):
        return not current_user.is_authenticated

    return pass_or_abort(condition)(f)

def authentication_redirect(func):
    """
    Decorator to redirect authenticated users to the index page.
    """

    @wraps(func)
    def decorator_func(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for("accounts.index"))
        return func(*args, **kwargs)

    return decorator_func
