"""Ports package — typed Protocol interfaces for all external dependencies.

Each port lives in its own module (one file per port, per spec).
The package re-exports every Protocol from its canonical submodule so both
``from app.ports import WeatherPort`` and
``from app.ports.weather import WeatherPort`` work.
"""

from app.ports.asr_tts import AsrTtsPort
from app.ports.embeddings import EmbeddingPort
from app.ports.image_diagnosis import ImageDiagnosisPort
from app.ports.llm import LLMPort
from app.ports.otp_delivery import OtpDeliveryPort
from app.ports.roster import AgronomistRosterPort
from app.ports.storage import StoragePort
from app.ports.weather import WeatherPort

__all__ = [
    "WeatherPort",
    "LLMPort",
    "EmbeddingPort",
    "ImageDiagnosisPort",
    "AsrTtsPort",
    "StoragePort",
    "AgronomistRosterPort",
    "OtpDeliveryPort",
]
