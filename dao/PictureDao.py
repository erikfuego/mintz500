from mintz500.models.Picture import Picture
from mintz500.models.exceptions.PictureNotFoundException import PictureNotFoundException


class PictureDao:
    def __init__(self, db):
        self.db = db
        pass

    def create_picture(self, name: str, content: str, user_id: str) -> Picture:
        picture_id = self.db.insert_one(
            {"name": name, "content": content, "user_id": user_id}
        ).inserted_id

        print("Successfully created picture, " + name)
        return Picture(picture_id, name, content, user_id)

    def get_picture(self, picture_id: str) -> Picture:
        picture_maybe: dict = self.db.find_one({"_id": picture_id})
        if picture_maybe is None:
            raise PictureNotFoundException
        return Picture(
            picture_maybe["_id"],
            picture_maybe["name"],
            picture_maybe["content"],
            picture_maybe["user_id"],
        )

    def get_pictures_by_user_id(self, user_id: str) -> [Picture]:
        result: list = self.db.find({"user_id": user_id})
        return list(
            map(
                lambda x: Picture(x["_id"], x["name"], x["content"], x["user_id"]),
                result,
            )
        )
