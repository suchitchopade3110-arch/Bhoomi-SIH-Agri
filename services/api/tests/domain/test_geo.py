"""Phase 1 geo-approach decision: pure haversine distance, no PostGIS.

See app/domain/geo.py module docstring for the decision rationale — the
project's Postgres image (pgvector/pgvector:pg16) has no PostGIS extension,
so spatial cluster queries (early_warning_alert_spec.md §3.3) fall back to
a bounding-box SQL pre-filter + exact haversine distance in Python.
"""

import pytest

from app.domain.geo import bounding_box, haversine_distance_km

# Erode, Tamil Nadu (approx.) and a point ~8km away, used by the spec's own
# "3 confirmed cases within 8km" worked example.
ERODE_LAT, ERODE_LON = 11.3410, 77.7172


def test_zero_distance_for_identical_coordinates():
    assert haversine_distance_km(ERODE_LAT, ERODE_LON, ERODE_LAT, ERODE_LON) == 0.0


def test_known_distance_delhi_to_mumbai():
    # Well-known great-circle distance, ~1150-1160 km depending on the
    # reference coordinates used; asserting a tolerant band.
    delhi = (28.6139, 77.2090)
    mumbai = (19.0760, 72.8777)
    distance = haversine_distance_km(*delhi, *mumbai)
    assert 1140 <= distance <= 1170


def test_distance_is_symmetric():
    a = (11.3410, 77.7172)
    b = (11.4200, 77.8000)
    assert haversine_distance_km(*a, *b) == haversine_distance_km(*b, *a)


def test_short_distance_matches_small_offset():
    # ~0.01 deg latitude offset at the equator-ish band is roughly 1.1km.
    near_lat, near_lon = ERODE_LAT + 0.01, ERODE_LON
    distance = haversine_distance_km(ERODE_LAT, ERODE_LON, near_lat, near_lon)
    assert 1.0 <= distance <= 1.3


def test_bounding_box_contains_center_point():
    min_lat, max_lat, min_lon, max_lon = bounding_box(ERODE_LAT, ERODE_LON, radius_km=10)
    assert min_lat < ERODE_LAT < max_lat
    assert min_lon < ERODE_LON < max_lon


def test_bounding_box_covers_points_within_radius():
    radius_km = 8.0
    min_lat, max_lat, min_lon, max_lon = bounding_box(ERODE_LAT, ERODE_LON, radius_km)

    # A point exactly within the radius per haversine must fall inside the
    # (necessarily looser) bounding box pre-filter.
    within_lat, within_lon = ERODE_LAT + 0.05, ERODE_LON
    assert haversine_distance_km(ERODE_LAT, ERODE_LON, within_lat, within_lon) < radius_km
    assert min_lat <= within_lat <= max_lat
    assert min_lon <= within_lon <= max_lon


@pytest.mark.parametrize("lat", [0.0, 45.0, -45.0, 89.0])
def test_bounding_box_never_divides_by_zero_near_poles(lat):
    # cos(lat) guard in bounding_box() must keep this finite even as
    # lat approaches 90 degrees.
    min_lat, max_lat, min_lon, max_lon = bounding_box(lat, 0.0, radius_km=10)
    assert all(map(lambda v: v == v, (min_lat, max_lat, min_lon, max_lon)))  # not NaN
