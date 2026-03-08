import requests
import random
import string

def test_register_and_login():
    base_url = "https://backend-toledo-1091873589468.europe-southwest1.run.app/api/v1"
    
    # Generate random user
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    username = f"testuser_{suffix}"
    email = f"test_{suffix}@example.com"
    password = "password123"
    
    print(f"--- Testing Registration for {username} ---")
    reg_url = f"{base_url}/auth/register"
    reg_data = {
        "email": email,
        "username": username,
        "password": password,
        "is_active": True,
        "is_admin": False
    }
    
    reg_resp = requests.post(reg_url, json=reg_data)
    print(f"Registration Status: {reg_resp.status_code}")
    print(f"Registration Response: {reg_resp.text}")
    
    if reg_resp.status_code == 200:
        print(f"--- Testing Login for {username} ---")
        login_url = f"{base_url}/auth/login"
        login_data = {
            "username": username,
            "password": password
        }
        login_resp = requests.post(login_url, data=login_data)
        print(f"Login Status: {login_resp.status_code}")
        print(f"Login Response: {login_resp.text}")
    else:
        print("Registration failed, skipping login test.")

if __name__ == "__main__":
    test_register_and_login()
