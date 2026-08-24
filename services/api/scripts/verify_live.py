import asyncio
import httpx
import uuid

async def test_flow():
    url = "http://127.0.0.1:8000/api/v1"
    async with httpx.AsyncClient() as client:
        # Register user
        phone = "+91" + uuid.uuid4().hex[:10]
        reg_res = await client.post(f"{url}/auth/register", json={
            "phone_number": phone,
            "full_name": "Test User",
            "role": "farmer",
            "preferred_language": "ta",
            "password": "testpassword123"
        })
        print(f"Auth Register Code: {reg_res.status_code}")
        if reg_res.status_code not in (200, 201):
            print("Register failed:", reg_res.text)
            return

        # Login
        login_res = await client.post(f"{url}/auth/login", json={
            "phone_number": phone,
            "password": "testpassword123"
        })
        print(f"Auth Login Code: {login_res.status_code}")
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create Farm
        farm_res = await client.post(f"{url}/farms", headers=headers, json={
            "farmer_id": "placeholder",
            "farm_name": "Test farm name",
            "village": "Chithode",
            "taluk": "Erode",
            "district": "Erode",
            "latitude": 11.34,
            "longitude": 77.71,
            "total_area_acres": 1.0,
            "primary_crop": "samba_paddy"
        })
        print(f"Create Farm Code: {farm_res.status_code}")
        farm_id = farm_res.json()["id"]

        # 1. GET /farms/{farm_id}/health
        health_res = await client.get(f"{url}/farms/{farm_id}/health", headers=headers)
        print(f"GET Health Route Code: {health_res.status_code}")
        print("Health body:", health_res.json())

        # 2. POST /farms/{farm_id}/diagnose
        diagnose_res = await client.post(f"{url}/farms/{farm_id}/diagnose", headers=headers, json={
            "image_asset_id": "test_asset_uuid",
            "description_text": "yellowing leaves"
        })
        print(f"POST Diagnose Route Code: {diagnose_res.status_code}")
        print("Diagnose body:", diagnose_res.json())

        # 3. GET /land/{farm_id}
        # First we need to submit land verification
        verify_res = await client.post(f"{url}/land/verify", headers=headers, json={
            "farm_id": farm_id,
            "survey_number": "142/3B",
            "patta_passbook_asset_id": "test_patta_uuid",
            "suggested_boundary": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [77.7214, 11.3412],
                        [77.7289, 11.3415],
                        [77.7285, 11.3478],
                        [77.7211, 11.3475],
                        [77.7214, 11.3412]
                    ]
                ]
            }
        })
        print(f"POST Land Verify Code: {verify_res.status_code}")
        
        land_res = await client.get(f"{url}/land/{farm_id}", headers=headers)
        print(f"GET Land Status Code: {land_res.status_code}")
        print("Land status body:", land_res.json())

        # 4. GET /officer/queue
        officer_res = await client.get(f"{url}/officer/queue", headers=headers)
        print(f"GET Officer Queue Code: {officer_res.status_code}")

        # 5. GET /agronomist/queue
        agronomist_res = await client.get(f"{url}/agronomist/queue", headers=headers)
        print(f"GET Agronomist Queue Code: {agronomist_res.status_code}")

if __name__ == "__main__":
    asyncio.run(test_flow())
