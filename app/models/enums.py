from enum import Enum


class UserRole(str, Enum):
    USER = "USER"
    AUTHOR = "AUTHOR"
    ADMIN = "ADMIN"