import requests

def test_login():
    url = "https://backend-toledo-1091873589468.europe-southwest1.run.app/api/v1/auth/login"
    data = {
        "username": "admin",
        "password": "123456"
    }
    
    print(f"Testing login at {url} with form-data...")
    response = requests.post(url, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    test_login()
