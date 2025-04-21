class MongoNotFoundError(Exception):
    def __init__(self, target_id):
        self.msg = f"Object with name {target_id} not found"
        super().__init__(self.msg)


class MongoInsertError(Exception):
    def __init__(self):
        self.msg = "Failed inserting document into MongoDB"
        super().__init__(self.msg)


class MongoUpdateError(Exception):
    def __init__(self, target_id):
        self.msg = f"Object with ID {target_id} was not updated"
        super().__init__(self.msg)


class MongoConnectionError(Exception):
    def __init__(self, msg: str = None):
        self.msg = "MongoDB connection failure." if msg is None else msg
        super().__init__(self.msg)