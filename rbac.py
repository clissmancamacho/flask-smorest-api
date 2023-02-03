from enum import Enum
from functools import wraps

from flask_jwt_extended import get_current_user, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError

from models import UserModel


# @check_access decorator function


def check_access(roles: [Enum] = []):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            # calling @jwt_required()
            verify_jwt_in_request()
            # fetching current user from db
            current_user: UserModel = get_current_user()
            user_roles = current_user.roles.all()
            # checking user roles
            for role in user_roles:
                if role.name in roles:
                    return f(*args, **kwargs)
            raise NoAuthorizationError("Role is not allowed.")
        return decorator_function
    return decorator
