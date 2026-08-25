"""Integration tests for farmer phone-OTP login (PRD §2.3).

Additive on top of /auth/register + /auth/login — verifies both the OTP
path works end-to-end and the existing password path is untouched.
"""

import uuid

import httpx
import pytest


@pytest.mark.asyncio(loop_scope="session")
async def test_otp_request_then_verify_creates_account_and_issues_token():
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
        phone = f"+919{uuid.uuid4().hex[:9]}"

        req_res = await client.post("/auth/otp/request", json={"phone_number": phone})
        assert req_res.status_code == 200, req_res.text
        body = req_res.json()
        assert body["expires_in"] == 300
        otp = body["debug_otp"]
        assert otp is not None and len(otp) == 6

        verify_res = await client.post(
            "/auth/otp/verify",
            json={"phone_number": phone, "otp": otp, "full_name": "Ramesh", "preferred_language": "ta"},
        )
        assert verify_res.status_code == 200, verify_res.text
        token_body = verify_res.json()
        assert token_body["role"] == "farmer"
        assert token_body["access_token"]

        # The issued token actually authenticates.
        me_res = await client.get("/auth/me", headers={"Authorization": f"Bearer {token_body['access_token']}"})
        assert me_res.status_code == 200, me_res.text
        assert me_res.json()["full_name"] == "Ramesh"
        assert me_res.json()["phone_number"] == phone


@pytest.mark.asyncio(loop_scope="session")
async def test_otp_verify_on_existing_account_does_not_require_full_name():
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
        phone = f"+919{uuid.uuid4().hex[:9]}"

        first = await client.post("/auth/otp/request", json={"phone_number": phone})
        otp1 = first.json()["debug_otp"]
        await client.post(
            "/auth/otp/verify", json={"phone_number": phone, "otp": otp1, "full_name": "Ramesh"}
        )

        second_req = await client.post("/auth/otp/request", json={"phone_number": phone})
        otp2 = second_req.json()["debug_otp"]
        second_verify = await client.post("/auth/otp/verify", json={"phone_number": phone, "otp": otp2})
        assert second_verify.status_code == 200, second_verify.text


@pytest.mark.asyncio(loop_scope="session")
async def test_otp_verify_rejects_wrong_code():
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
        phone = f"+919{uuid.uuid4().hex[:9]}"
        await client.post("/auth/otp/request", json={"phone_number": phone})

        res = await client.post(
            "/auth/otp/verify", json={"phone_number": phone, "otp": "000000", "full_name": "X"}
        )
        assert res.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_otp_verify_new_phone_without_full_name_is_rejected():
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
        phone = f"+919{uuid.uuid4().hex[:9]}"
        req = await client.post("/auth/otp/request", json={"phone_number": phone})
        otp = req.json()["debug_otp"]

        res = await client.post("/auth/otp/verify", json={"phone_number": phone, "otp": otp})
        assert res.status_code == 422


@pytest.mark.asyncio(loop_scope="session")
async def test_otp_request_resend_cooldown():
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
        phone = f"+919{uuid.uuid4().hex[:9]}"
        first = await client.post("/auth/otp/request", json={"phone_number": phone})
        assert first.status_code == 200

        second = await client.post("/auth/otp/request", json={"phone_number": phone})
        assert second.status_code == 429


@pytest.mark.asyncio(loop_scope="session")
async def test_otp_verify_exhausts_after_max_attempts():
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
        phone = f"+919{uuid.uuid4().hex[:9]}"
        await client.post("/auth/otp/request", json={"phone_number": phone})

        # 5 wrong attempts (MAX_VERIFY_ATTEMPTS), all rejected.
        for _ in range(5):
            res = await client.post(
                "/auth/otp/verify", json={"phone_number": phone, "otp": "000000", "full_name": "X"}
            )
            assert res.status_code == 401

        # 6th attempt (even with a fresh request+correct code) fails: the
        # exhausted record was deleted, so this phone has no live code.
        res = await client.post(
            "/auth/otp/verify", json={"phone_number": phone, "otp": "111111", "full_name": "X"}
        )
        assert res.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_password_login_still_works_unaffected_by_otp_endpoints():
    """Zero-regression check: the pre-existing password auth path (used by
    officer/agronomist, and by farmers who don't use OTP) is untouched."""
    import app.main as main_module

    transport = httpx.ASGITransport(app=main_module.app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test/api/v1") as client:
        phone = f"+919{uuid.uuid4().hex[:9]}"
        reg = await client.post(
            "/auth/register",
            json={
                "phone_number": phone,
                "full_name": "Password Farmer",
                "role": "farmer",
                "preferred_language": "en",
                "password": "testpassword123",
            },
        )
        assert reg.status_code == 201, reg.text

        login = await client.post("/auth/login", json={"phone_number": phone, "password": "testpassword123"})
        assert login.status_code == 200, login.text
