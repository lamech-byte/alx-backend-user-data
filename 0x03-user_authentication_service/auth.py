"""auth module
"""
import bcrypt

def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The password string to hash.

    Returns:
        bytes: The hashed password bytes.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

if __name__ == "__main__":
    print(_hash_password("Hello Holberton"))
