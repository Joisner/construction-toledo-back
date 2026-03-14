import requests, json

BASE_URL = "https://backend-toledo-1091873589468.europe-southwest1.run.app"

# 1. Login
login_data = {"username": "admin", "password": "123456"}
res = requests.post(f"{BASE_URL}/api/v1/auth/login", data=login_data)
print("Login status:", res.status_code)
token = res.json().get("access_token")
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

# 2. Test POST Invoice with empty clientEmail
invoice_data = {
    "number": "FAC-TEST-001",
    "date": "2026-03-10T10:00:00",
    "clientName": "Cliente Test",
    "clientAddress": "Calle de prueba 123",
    "clientDNI": "",
    "clientPhone": "",
    "clientEmail": "",
    "items": [{"description": "Servicio de prueba", "amount": 100.0}],
    "taxRate": 21.0,
    "iban": ""
}

print("\n--- Test 1: POST invoice with empty clientEmail ---")
inv_res = requests.post(f"{BASE_URL}/api/v1/invoices/", headers=headers, json=invoice_data)
print("Status:", inv_res.status_code)
print("Response:", json.dumps(inv_res.json(), indent=2))

# 3. Test POST Invoice with null clientEmail
invoice_data2 = {
    "number": "FAC-TEST-002",
    "date": "2026-03-10T10:00:00",
    "clientName": "Cliente Test 2",
    "clientAddress": "Calle de prueba 456",
    "items": [{"description": "Otro servicio", "amount": 200.0}],
    "taxRate": 21.0
}

print("\n--- Test 2: POST invoice without clientEmail field ---")
inv_res2 = requests.post(f"{BASE_URL}/api/v1/invoices/", headers=headers, json=invoice_data2)
print("Status:", inv_res2.status_code)
print("Response:", json.dumps(inv_res2.json(), indent=2))

# 4. Test GET invoices to confirm they were created
print("\n--- Test 3: GET all invoices ---")
get_res = requests.get(f"{BASE_URL}/api/v1/invoices/", headers=headers)
print("Status:", get_res.status_code)
print("Response:", json.dumps(get_res.json(), indent=2))
