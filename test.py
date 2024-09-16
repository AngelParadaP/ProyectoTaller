import bcrypt

password = "4321"
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

print(hashed_password)
print(len(hashed_password))