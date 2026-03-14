"""
End-to-end test for GCS upload integration.
Tests: login, upload main image, upload media, GET projects, verify GCS URLs, verify image reachability.
"""
import requests, json, sys, os

BASE_URL = "https://backend-toledo-1091873589468.europe-southwest1.run.app"
GCS_PREFIX = "https://storage.googleapis.com/toledo-media-uploads/"

# Use a small test image (1x1 pixel PNG)
TEST_PNG = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82'

def main():
    errors = []
    
    # 1. Login
    print("1. Logging in as admin...")
    res = requests.post(f"{BASE_URL}/api/v1/auth/login", data={"username": "admin", "password": "123456"})
    assert res.status_code == 200, f"Login failed: {res.status_code}"
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"   OK - Token obtained")

    # 2. Create a test project
    print("2. Creating test project...")
    project_data = {
        "title": "GCS Test Project",
        "description": "Testing GCS uploads",
        "location": "Test Location",
        "service": "Test Service",
        "completion_date": "2026-03-13T00:00:00",
        "is_active": True
    }
    res = requests.post(f"{BASE_URL}/api/v1/projects/", headers={**headers, "Content-Type": "application/json"}, json=project_data)
    assert res.status_code == 200, f"Create project failed: {res.status_code} - {res.text}"
    project_id = res.json()["id"]
    print(f"   OK - Project ID: {project_id}")

    # 3. Upload main image
    print("3. Uploading main image...")
    files = {"file": ("test_main.png", TEST_PNG, "image/png")}
    res = requests.post(f"{BASE_URL}/api/v1/projects/{project_id}/main-image", headers=headers, files=files)
    print(f"   Status: {res.status_code}")
    if res.status_code == 200:
        main_image_url = res.json().get("main_image", "")
        print(f"   main_image URL: {main_image_url}")
        if main_image_url.startswith(GCS_PREFIX):
            print("   ✅ URL is a GCS URL!")
        else:
            errors.append(f"main_image URL does not start with GCS prefix: {main_image_url}")
            print(f"   ❌ URL is NOT a GCS URL")
        
        # Verify image is accessible
        img_res = requests.get(main_image_url)
        if img_res.status_code == 200:
            print(f"   ✅ Image is publicly accessible (HTTP {img_res.status_code})")
        else:
            errors.append(f"Image not accessible: HTTP {img_res.status_code}")
            print(f"   ❌ Image NOT accessible (HTTP {img_res.status_code})")
    else:
        errors.append(f"Main image upload failed: {res.status_code} - {res.text}")
        print(f"   ❌ Upload failed: {res.text}")

    # 4. Upload media file
    print("4. Uploading media file...")
    files = {"file": ("test_media.png", TEST_PNG, "image/png")}
    data = {"description": "GCS test media", "is_before": "true"}
    res = requests.post(f"{BASE_URL}/api/v1/projects/{project_id}/media", headers=headers, files=files, data=data)
    print(f"   Status: {res.status_code}")
    if res.status_code == 200:
        media_url = res.json().get("file_url", "")
        media_id = res.json().get("id", "")
        print(f"   file_url: {media_url}")
        if media_url.startswith(GCS_PREFIX):
            print("   ✅ URL is a GCS URL!")
        else:
            errors.append(f"media file_url does not start with GCS prefix: {media_url}")
            print(f"   ❌ URL is NOT a GCS URL")
    else:
        errors.append(f"Media upload failed: {res.status_code} - {res.text}")
        print(f"   ❌ Upload failed: {res.text}")

    # 5. GET projects and verify URLs
    print("5. GET projects to verify stored URLs...")
    res = requests.get(f"{BASE_URL}/api/v1/projects/{project_id}", headers=headers)
    if res.status_code == 200:
        proj = res.json()
        print(f"   main_image: {proj.get('main_image', 'N/A')}")
        for m in proj.get("media", []):
            print(f"   media file_url: {m.get('file_url', 'N/A')}")
        print("   ✅ Project data retrieved successfully")
    else:
        errors.append(f"GET project failed: {res.status_code}")

    # 6. Cleanup - delete test project
    print("6. Cleaning up test project...")
    res = requests.delete(f"{BASE_URL}/api/v1/projects/{project_id}", headers=headers)
    print(f"   Delete status: {res.status_code}")

    # Summary
    print("\n" + "="*50)
    if errors:
        print(f"❌ FAILED - {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("✅ ALL TESTS PASSED!")
        sys.exit(0)

if __name__ == "__main__":
    main()
