from mintz500.models.exceptions.ValidationException import ValidationException


class Validator:
    @staticmethod
    def validate_signup(username: str, password: str):
        errors = []
        if is_none_or_empty(username):
            errors.append("username cannot be blank")
        if is_none_or_empty(password):
            errors.append("password cannot be blank")
        if len(errors):
            raise ValidationException(errors)

    @staticmethod
    def validate_login(username: str, password: str):
        errors = []
        if is_none_or_empty(username):
            errors.append("username cannot be blank")
        if is_none_or_empty(password):
            errors.append("password cannot be blank")
        if len(errors):
            raise ValidationException(errors)


def is_none_or_empty(var) -> bool:
    return var is None or not len(var)
