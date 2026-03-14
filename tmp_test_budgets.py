import requests

BASE_URL = "https://backend-toledo-1091873589468.europe-southwest1.run.app"

# 1. Login
login_data = {"username": "admin", "password": "123456"}
res = requests.post(f"{BASE_URL}/api/v1/auth/login", data=login_data)
token = res.json().get("access_token")

# 2. Get Budgets
headers = {"Authorization": f"Bearer {token}"}
print("Requesting budgets...")
budgets_res = requests.get(f"{BASE_URL}/api/v1/budgets/", headers=headers)

print("Status:", budgets_res.status_code)
try:
    print("Response:", budgets_res.json())
except Exception:
    print("Response text:", budgets_res.text)
