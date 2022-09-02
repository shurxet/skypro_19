from flask import abort
import base64
import hashlib
import hmac


from dao.user import UserDAO
from helpers.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def create(self, user_data):
        if user_data["role"] == "superuser":
            abort(403)
        # Здесь заменяется нехешированный пароль на хешированный
        # Функция generate_password() фозвращает хешированный пароль
        user_data["password"] = self.generate_password(user_data["password"])
        return self.dao.create(user_data)

    def update(self, user_data):
        user_data["password"] = self.generate_password(user_data["password"])

        uid = user_data.get("id")
        user = self.get_one(uid)

        user.username = user_data.get("username")
        user.password = user_data.get("password")
        user.role = user_data.get("role")

        self.dao.update(user)

        return user

    def delete(self, user_data):
        self.dao.delete(user_data)

    # Функция которая принимает пароль и возвращает закодированный пароль то есть хеш
    def generate_password(self, password):

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return base64.b64encode(hash_digest)


    def compare_passwords(self, password_hash, other_password) -> bool:
        decoded_digest = base64.b64decode(password_hash)

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return hmac.compare_digest(decoded_digest, hash_digest)
