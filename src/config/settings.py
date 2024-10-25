from dataclasses import dataclass

@dataclass
class SecurityConfig:
    USERSLISTLOGIN: bool = False  # If True, shows dropdown instead of text input
    STRONGPASSWORD: bool = False    # Requir2es complex password
    STRONGLENGTH: int = 6         # Minimum password length
    PASSWORDTRIES: int = 5        # Max login attempts
    PASSWORDLOCKTIME: int = 60    # Lock duration in minutes
    SPECIAL_CHARS: str = "!@#$%^&*()_+-=[]{}|;:,.<>?"

config = SecurityConfig()
