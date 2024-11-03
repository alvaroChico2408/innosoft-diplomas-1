
import typing as t
import secrets


def unique_security_token() -> t.AnyStr:
    """
    Generate a unique security token that does not already
    exist in the `UserSecurityToken` model.

    Recursively generates a new token if a collision is found.

    Returns:
        str: A unique security token.
    """
    from .models import UserSecurityToken

    generated_token = secrets.token_hex()

    token_exist = UserSecurityToken.is_exists(generated_token)

    if not token_exist:
        return generated_token

    return unique_security_token()