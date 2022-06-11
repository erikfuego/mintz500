class Picture:
    def __init__(self, id: str, content: str, name: str, user_id: str):
        self.id = id
        self.name = name
        self.content = content
        self.user_id = user_id

    # def __repr__(self):
    #     return f"Username: <{self.username}>"
