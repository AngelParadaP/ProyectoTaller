import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()


def check_password(input_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)
