from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")
new_hash = "$pbkdf2-sha256$29000$5nyvtTbmnJMSwpgTIkRIKQ$0vCvXEAnOXbMpiJqRH.LLTjbVxsOdX858xTtOiJTOdw"
password = "123456"

is_correct = pwd_context.verify(password, new_hash)
print(f"Is password '{password}' correct for NEW hash? {is_correct}")
