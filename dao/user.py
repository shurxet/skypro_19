from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        return self.session.query(User).get(uid)

    def get_all(self):
        return self.session.query(User).all()

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def create(self, user_data):
        new_user = User(**user_data)

        self.session.add(new_user)
        self.session.commit()

        return new_user

    def update(self, data):
        self.session.add(data)
        self.session.commit()

        return data

    def delete(self, uid):
        user = self.get_one(uid)

        self.session.delete(user)
        self.session.commit()
