import re
from typing import Tuple
from src.config.settings import config

class InputValidator:
    @staticmethod
    def validate_login_input(user_name: str, password: str) -> Tuple[bool, str]:
        if user_name.strip() == "" or password.strip() == "":
            return False, "Username or Password cannot be blank"

        if len(password) < config.STRONGLENGTH:
            return False, f"Password must be at least {config.STRONGLENGTH} characters long"

        if config.STRONGPASSWORD:
            if not re.search(r"[A-Za-z]", password):
                return False, "Password must contain at least one letter"
            if not re.search(r"\d", password):
                return False, "Password must contain at least one number"
            if not re.search(f"[{re.escape(config.SPECIAL_CHARS)}]", password):
                return False, "Password must contain at least one special character"

        return True, ""