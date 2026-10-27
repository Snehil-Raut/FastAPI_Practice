from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def Hash(password: str):
    return password_hash.hash(password)

def verify_pass(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)  # verifys if user palin password after hased is matches the hasehd one in db 
    