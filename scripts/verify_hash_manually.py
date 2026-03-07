from passlib.context import CryptContext

def verify():
    pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")
    password = "admin12345"
    stored_hash = "$pbkdf2-sha256$29000$EKK0do4xJgQAwNjbew9hzA$zxrqPqH/9Vuo96B6VMIlj2yd3Bq3jpTU1jqOU97ZUCE"
    
    is_valid = pwd_context.verify(password, stored_hash)
    print(f"Is valid: {is_valid}")
    
    # Generate a fresh one just to see
    fresh_hash = pwd_context.hash(password)
    print(f"Fresh hash example: {fresh_hash}")

if __name__ == "__main__":
    verify()
