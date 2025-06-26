import bcrypt
salt_rounds = 10
from repository.user import UserRepository


class AuthService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def _verify_password(self, input_password, hashed_password):
        if bcrypt.checkpw(input_password, hashed_password):
            return True
        return False

    def get_user(self, email_id):
        user = self.user_repository.get_item_from_table(email_id)

        if user.get("ResponseMetadata").get("HTTPStatusCode") != 200:
            raise Exception("Error occurred while fetching data from DB")

        if user.get("Attributes", None) is None:
            return None

        return user.get("Attributes")

    def verify_credentials(self, email_id, password):
        user = self.get_user(email_id)

        if user is None:
            raise Exception("Invalid username or password")

        if not self._verify_password(password, user["hashed_password"]):
            raise Exception("Invalid username or password")

        del user["hashed_password"]

        return {"status": "VERIFIED", "user": user}
