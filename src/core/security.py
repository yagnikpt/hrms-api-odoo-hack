import bcrypt


def hash_password(password: str) -> str:
    # bcrypt truncates to 72 bytes; truncate manually to avoid errors
    truncated = password.encode("utf-8")[:72]
    return bcrypt.hashpw(truncated, bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    # Truncate the same way for verification
    truncated = password.encode("utf-8")[:72]
    return bcrypt.checkpw(truncated, hashed.encode("utf-8"))
