"""Integration tests for GET /farms (list farms owned by the authenticated farmer).

Without this endpoint, any client holding only a JWT (e.g. right after
login) has no way to discover which farm_id to call ``/farms/{id}/...``
against — it previously had to already know the UUID from a prior
``POST /farms`` response.
"""

import uuid

import httpx
import pytest


async def _register_and_login(client: httpx.AsyncClient) -> tuple[str, dict[str, str]]:
    phone = f"+919{uuid.uuid4().hex[:9]}"
    reg = await client.post(
        "/auth/register",
        json={
            "phone_number": phone,
            "full_name": "Test Farmer",
            "role": "farmer",
            "preferred_language": "en",
            "password": "testpassword123",
        },
    )
    assert reg.status_code == 201, reg.text
    farmer_id = reg.json()["id"]
    login = await client.post(
        "/auth/login",
        json={"phone_number": phone, "password": "testpassword123"},
    )
    assert login.status_code == 200, login.text
    token = login.json()["access_token"]
    return farmer_id, {"Authorization": f"Bearer {token}"}


async def _create_farm(client: httpx.AsyncClient, farmer_id: str, headers: dict[str, str], name: str) -> str:
    res = await client.post(
        "/farms",
        headers=headers,
        json={
            "farmer_id": farmer_id,
            "crop": "samba_paddy",
            "growth_stage": "vegetative",
            "region": name,
        },
    )
    assert res.status_code == 201, res.text
    return res.json()["id"]


@pytest.mark.asyncio(loop_scope="session")
async def test_list_farms_returns_only_own_farms():
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
        farmer_id, headers = await _register_and_login(client)
        other_farmer_id, other_headers = await _register_and_login(client)

        farm_id = await _create_farm(client, farmer_id, headers, "Kaveri Delta Field 1")
        second_farm_id = await _create_farm(client, farmer_id, headers, "Kaveri Delta Field 2")
        await _create_farm(client, other_farmer_id, other_headers, "Someone Else's Field")

        res = await client.get("/farms", headers=headers)
        assert res.status_code == 200, res.text
        farms = res.json()

        returned_ids = {f["id"] for f in farms}
        assert returned_ids == {farm_id, second_farm_id}
        assert all(f["farmer_id"] == farmer_id for f in farms)


@pytest.mark.asyncio(loop_scope="session")
async def test_list_farms_empty_for_new_farmer():
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
        _farmer_id, headers = await _register_and_login(client)

        res = await client.get("/farms", headers=headers)
        assert res.status_code == 200, res.text
        assert res.json() == []


@pytest.mark.asyncio(loop_scope="session")
async def test_list_farms_requires_auth():
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
        res = await client.get("/farms")
        assert res.status_code in (401, 403)
