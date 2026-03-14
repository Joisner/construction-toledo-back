import requests

BASE_URL = "https://backend-toledo-1091873589468.europe-southwest1.run.app"

# 1. Login
login_data = {"username": "admin", "password": "123456"}
res = requests.post(f"{BASE_URL}/api/v1/auth/login", data=login_data)
print("Login status:", res.status_code)
token = res.json().get("access_token")

# 2. Get Invoices
headers = {"Authorization": f"Bearer {token}"}
print("\nRequesting invoices...")
inv_res = requests.get(f"{BASE_URL}/api/v1/invoices/", headers=headers)
print("Status:", inv_res.status_code)
try:
    print("Response:", inv_res.json())
except Exception:
    print("Response text:", inv_res.text)

# 3. Also test quotes endpoint
print("\nRequesting quotes...")
quotes_res = requests.get(f"{BASE_URL}/api/v1/quotes/", headers=headers)
print("Status:", quotes_res.status_code)
try:
    print("Response:", quotes_res.json())
except Exception:
    print("Response text:", quotes_res.text)

# 4. Also test projects endpoint  
print("\nRequesting projects...")
proj_res = requests.get(f"{BASE_URL}/api/v1/projects/", headers=headers)
print("Status:", proj_res.status_code)
try:
    print("Response:", proj_res.json())
except Exception:
    print("Response text:", proj_res.text)
