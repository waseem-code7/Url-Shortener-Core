import bcrypt
salt_rounds = 10
from repository.user import UserRepository


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def _hash_password(self, password):
        salt = bcrypt.gensalt(rounds=salt_rounds)
        hashed_password = bcrypt.hashpw(password, salt)

    def _verify_password(self, input_password, hashed_password):
        if bcrypt.checkpw(input_password, hashed_password):
            return True
        return False

    def user_exists(self, email_id):
        user = self.user_repository.get_item_from_table(email_id)

        if user.get("ResponseMetadata").get("HTTPStatusCode") != 200:
            raise Exception("Error occurred while fetching data from DB")

        if user.get("Attributes", None) is None:
            return False

        return True

    def create_new_user(self, user_details: dict):
        email = user_details.get("email")
        password = user_details.get("password")
        hash_password = self._hash_password(password)

        if self.user_exists(email):
            raise Exception("Duplicate email id found")
        del user_details["password"]

        user_details["hashed_password"] = hash_password

        self.user_repository.put_item(user_details, "NONE")

    def change_password(self, email, old_password, new_password):
        user = self.user_repository.get_item(email)

        if user is None or user.get("ResponseMetadata").get("HTTPStatusCode") != 200:
            raise Exception("Error occurred while fetching data from DB")

        hashed_password = user["Attributes"]["hashed_password"]

        if not self._verify_password(old_password, hashed_password):
            raise Exception("Invalid password provided")

        hash_password = self._hash_password(new_password)

        self.user_repository.update_param_in_record(email, "hashed_password", hash_password, "NONE")






