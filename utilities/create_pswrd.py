import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

password = 'hola'
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=8)).decode()

print(hashed_password)