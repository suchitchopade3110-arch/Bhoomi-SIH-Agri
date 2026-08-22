"""Smoke test (Phase 5 DoD item 5): boots the app in-process, hits the root
and health endpoints, and confirms the database is actually reachable
through it — the thing a judge can run on the demo box before judging
starts, without a separate uvicorn process.

Run as:  python -m scripts.smoke   (via `make smoke`, which also runs
migrate + seed + ingest-corpus first)
"""

import asyncio
import sys

import httpx

from app.main import app

BASE_URL = "http://smoke/api/v1"


async def _check(client: httpx.AsyncClient, method: str, path: str, **kwargs) -> httpx.Response:
    resp = await client.request(method, path, **kwargs)
    status = "OK" if resp.is_success else "FAIL"
    print(f"[{status}] {method} {path} -> {resp.status_code}")
    return resp


async def run_smoke() -> bool:
    transport = httpx.ASGITransport(app=app)
    ok = True
    async with httpx.AsyncClient(transport=transport, base_url="http://smoke") as client:
        resp = await _check(client, "GET", "/")
        ok &= resp.status_code == 200

        resp = await _check(client, "GET", "/health")
        ok &= resp.status_code == 200

    async with httpx.AsyncClient(transport=transport, base_url=BASE_URL) as client:
        # A real DB round-trip through the full stack: register a throwaway
        # user, log in, hit a health endpoint that requires Postgres.
        import uuid

        phone = "+91" + uuid.uuid4().hex[:10]
        resp = await _check(
            client,
            "POST",
            "/auth/register",
            json={
                "phone_number": phone,
                "full_name": "Smoke Test",
                "role": "farmer",
                "preferred_language": "ta",
                "password": "smoke-test-pass",
            },
        )
        ok &= resp.status_code == 201

        resp = await _check(
            client, "POST", "/auth/login", json={"phone_number": phone, "password": "smoke-test-pass"}
        )
        ok &= resp.status_code == 200
        if resp.status_code == 200:
            token = resp.json()["access_token"]
            resp = await _check(
                client,
                "POST",
                "/farms",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "farmer_id": "placeholder",
                    "farm_name": "Smoke Test Farm",
                    "village": "Chithode",
                    "taluk": "Erode",
                    "district": "Erode",
                    "latitude": 11.34,
                    "longitude": 77.71,
                    "total_area_acres": 1.0,
                    "primary_crop": "samba_paddy",
                },
            )
            ok &= resp.status_code == 201
            if resp.status_code == 201:
                farm_id = resp.json()["id"]
                resp = await _check(
                    client, "GET", f"/farms/{farm_id}/health", headers={"Authorization": f"Bearer {token}"}
                )
                ok &= resp.status_code == 200 and resp.json()["band"] == "unrated"

    return bool(ok)


def main() -> None:
    ok = asyncio.run(run_smoke())
    if ok:
        print("\nSmoke test passed — app boots, DB reachable, core endpoints respond.")
        sys.exit(0)
    print("\nSmoke test FAILED — see failures above.")
    sys.exit(1)


if __name__ == "__main__":
    main()
