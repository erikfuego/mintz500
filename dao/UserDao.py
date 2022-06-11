from mintz500.Utils import hash_str
from mintz500.models.User import User
from mintz500.models.exceptions import UserNotFoundException


class UserDao:
    def __init__(self, db):
        self.db = db
        pass

    def create_user(self, username: str, password: str) -> User:
        hashed_password = hash_str(password)
        self.db.insert_one(
            {"_id": username, "username": username, "password": hashed_password}
        )

        print("Successfully created user, " + username)
        return User(username, hashed_password)

    def get_user(self, username: str) -> User:
        user_maybe = self.db.find_one({"_id": username})
        if user_maybe is None:
            raise UserNotFoundException
        return User(user_maybe["username"], user_maybe["password"])
