import json
from typing import Optional, List, Tuple
from datetime import datetime, timedelta
from src.models.user import User
from src.config.settings import config

class UserRepository:
    def __init__(self, file_path: str = "users.json"):
        self.file_path = file_path

    def get_users(self) -> List[User]:
        try:
            with open(self.file_path) as users_file:
                users_data = json.load(users_file)
                users = []
                for user_data in users_data:
                    user = User(**user_data)
                    if isinstance(user.locked_until, str):
                        user.locked_until = datetime.fromisoformat(user.locked_until)
                    users.append(user)
                return users
        except FileNotFoundError:
            return []

    def save_users(self, users: List[User]) -> None:
        users_data = []
        for user in users:
            user_dict = user.__dict__
            if user.locked_until:
                user_dict['locked_until'] = user.locked_until.isoformat()
            users_data.append(user_dict)
        
        with open(self.file_path, 'w') as users_file:
            json.dump(users_data, users_file, indent=4)

    def find_by_credentials(self, user_name: str, password: str) -> Tuple[Optional[User], str]:
        users = self.get_users()
        for user in users:
            if user.user_name == user_name:
                if user.locked_until and user.locked_until > datetime.now():
                    remaining_time = (user.locked_until - datetime.now()).seconds // 60
                    return None, f"Account is locked. Try again in {remaining_time} minutes."

                if user.password == password:
                    user.login_attempts = 0
                    self.save_users(users)
                    return user, ""
                else:
                    user.login_attempts += 1
                    if user.login_attempts >= config.PASSWORDTRIES:
                        user.locked_until = datetime.now() + timedelta(minutes=config.PASSWORDLOCKTIME)
                        self.save_users(users)
                        return None, f"Account locked for {config.PASSWORDLOCKTIME} minutes due to too many failed attempts."
                    self.save_users(users)
                    return None, f"Incorrect password. {config.PASSWORDTRIES - user.login_attempts} attempts remaining."
        return None, "User not found."

    def get_all_usernames(self) -> List[str]:
        users = self.get_users()
        return [user.user_name for user in users]

    def get_user_by_username(self, username: str) -> Optional[User]:
        users = self.get_users()
        for user in users:
            if user.user_name == username:
                return user
        return None
