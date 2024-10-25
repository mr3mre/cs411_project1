from typing import Tuple, Optional, List
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.validators.input_validator import InputValidator

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.validator = InputValidator()

    def authenticate(self, user_name: str, password: str) -> Tuple[bool, Optional[User], str]:
        is_valid, error_message = self.validator.validate_login_input(user_name, password)
        if not is_valid:
            return False, None, error_message

        user, message = self.user_repository.find_by_credentials(user_name, password)
        if user:
            return True, user, ""
        
        return False, None, message

    def get_usernames(self) -> List[str]:
        return self.user_repository.get_all_usernames()
