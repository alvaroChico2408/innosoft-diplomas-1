
import typing as t
import secrets
import os
import uuid
from werkzeug.utils import secure_filename


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


def remove_existing_file(path=None):
    """
    Remove an existing file from the filesystem.
    """
    if os.path.isfile(path=path):
        os.remove(path)
        
def get_unique_filename(filename: t.Text = None) -> t.Text:
    """
    Generate a unique filename by appending a `uuid4()` to the original file extension.

    Returns:
        str: A new filename with a unique `uuid4()` or None if no filename is provided.
    """
    if not filename:
        return None

    filename = secure_filename(filename).split(".")
    return "{}.{}".format(str(uuid.uuid4()), filename[len(filename) - 1])