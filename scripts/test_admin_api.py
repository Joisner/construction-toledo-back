import requests

def test_admin_api_register():
    base_url = "https://backend-toledo-1091873589468.europe-southwest1.run.app/api/v1"
    
    username = "admin_api"
    email = "admin_api@construction-toledo.com"
    password = "password123"
    
    print(f"--- Registering {username} via API ---")
    reg_resp = requests.post(f"{base_url}/auth/register", json={
        "email": email,
        "username": username,
        "password": password,
        "is_active": True,
        "is_admin": True
    })
    print(f"Status: {reg_resp.status_code}, Body: {reg_resp.text}")
    
    if reg_resp.status_code == 200:
        print(f"--- Logging in with {username} ---")
        login_resp = requests.post(f"{base_url}/auth/login", data={
            "username": username,
            "password": password
        })
        print(f"Status: {login_resp.status_code}, Body: {login_resp.text}")

if __name__ == "__main__":
    test_admin_api_register()
