import requests

def test_admin_login():
    url = "https://backend-toledo-1091873589468.europe-southwest1.run.app/api/v1/auth/login"
    data = {
        "username": "admin",
        "password": "123456"
    }
    print(f"Testing login for 'admin'...")
    resp = requests.post(url, data=data)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text}")

if __name__ == "__main__":
    test_admin_login()
