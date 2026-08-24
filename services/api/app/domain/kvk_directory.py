"""Static KVK (Krishi Vigyan Kendra) center directory (PRD §5.11).

Pure reference data — no I/O — same pattern as ``farm_reference_data.py``.
Backs Phase 2's next-available routing (``app/domain/routing.py``) until a
real officer/agronomist-capacity model exists in the schema (PRD §10 risk
#10). ``kvk_erode`` is kept as the first entry so it stays the routing
result whenever it is in fact the nearest/least-loaded center, matching the
single-center behavior every caller previously hardcoded
(``DEFAULT_ASSIGNED_AGRONOMIST`` in ``escalation_service.py`` /
``diagnosis_service.py``).

Coordinates are approximate town-center points for each KVK's host town —
precise enough to rank "nearest center" for routing, not survey-grade.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class KvkCenter:
    center_id: str
    name: str
    district: str
    latitude: float
    longitude: float
    capacity: int = 15


KVK_CENTERS: list[KvkCenter] = [
    KvkCenter("agronomist:kvk_erode", "ICAR-KVK Erode", "Erode", 11.3410, 77.7172),
    KvkCenter("agronomist:kvk_coimbatore", "ICAR-KVK Coimbatore", "Coimbatore", 11.0168, 76.9558),
    KvkCenter("agronomist:kvk_madurai", "TNAU KVK Madurai", "Madurai", 9.9252, 78.1198),
    KvkCenter("agronomist:kvk_salem", "ICAR-KVK Salem", "Salem", 11.6643, 78.1460),
    KvkCenter("agronomist:kvk_thanjavur", "TNAU KVK Thanjavur", "Thanjavur", 10.7870, 79.1378),
]

DEFAULT_KVK_CENTER_ID = KVK_CENTERS[0].center_id
