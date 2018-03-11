class Chairman:
    def __init__(self, db, token):
        self.db = db
        self.token = token

    def shoot(self, name):
        self.db.child("test")
        data = {"name": name}
        self.db.child("test").push(data, self.token)

    def listen_to_photo_taking(self):
        pass

    def catch(self):
        test = self.db.child("test").get(self.token)
        print(test.val()["test"])


if __name__ == '__main__':
   pass