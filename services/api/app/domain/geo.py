"""Pure domain logic for great-circle distance between farm coordinates.

Backs the SIH26131 alert cluster query (spec §3.3) and any future
proximity-based routing (Phase 2 next-available routing). No I/O: the
caller (a repository) fetches candidate ``(latitude, longitude)`` pairs and
hands them in here. Same inputs, same output, always.

Decision (Phase 1 geo-approach): early_warning_alert_spec.md §3.3 specifies
a PostGIS ``ST_DWithin``/``ST_Distance`` query, but the project's actual
Postgres image is ``pgvector/pgvector:pg16`` — pgvector only, no PostGIS
(see infra/init-db.sql, where the `CREATE EXTENSION postgis` line is
commented out as "available when using postgis-enabled image"). Standing
up PostGIS is real infra work (new image, extension, a geometry column +
migration, GiST index) that nothing else in the codebase currently needs.
Until that infra change is made, spatial queries use the existing
``latitude``/``longitude`` float columns on ``farms``: the repository
pre-filters candidates with a cheap bounding-box WHERE clause (or a
district/taluk filter), then this module computes exact haversine distance
in Python to apply the radius cutoff. This keeps repositories on plain
SQLAlchemy with zero new extension dependency, at the cost of an
in-Python distance pass over the pre-filtered candidate set — acceptable
at this project's scale. Revisit if farm density per district grows large
enough that the bounding-box pre-filter stops being selective.
"""

from math import asin, cos, radians, sin, sqrt

EARTH_RADIUS_KM = 6371.0088


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in kilometers between two WGS84 coordinates."""
    lat1_r, lon1_r, lat2_r, lon2_r = radians(lat1), radians(lon1), radians(lat2), radians(lon2)
    dlat = lat2_r - lat1_r
    dlon = lon2_r - lon1_r
    a = sin(dlat / 2) ** 2 + cos(lat1_r) * cos(lat2_r) * sin(dlon / 2) ** 2
    return round(2 * EARTH_RADIUS_KM * asin(sqrt(a)), 4)


def bounding_box(lat: float, lon: float, radius_km: float) -> tuple[float, float, float, float]:
    """Cheap lat/lon bounding box (min_lat, max_lat, min_lon, max_lon) for a
    pre-filter WHERE clause, ahead of the exact ``haversine_distance_km`` cut.

    Longitude degrees shrink toward the poles; guards against a zero
    ``cos(lat)`` at the poles (not a real concern for Indian farm
    coordinates, but keeps the function total).
    """
    lat_delta = radius_km / EARTH_RADIUS_KM * (180 / 3.141592653589793)
    lon_denominator = max(cos(radians(lat)), 1e-9)
    lon_delta = radius_km / (EARTH_RADIUS_KM * lon_denominator) * (180 / 3.141592653589793)
    return (lat - lat_delta, lat + lat_delta, lon - lon_delta, lon + lon_delta)
