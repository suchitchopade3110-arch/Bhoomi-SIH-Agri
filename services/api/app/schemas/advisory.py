"""Advisory and Citation schemas for Grounded 5-Point Advisory."""

from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.common import SpokenResponseMixin


class Citation(BaseModel):
    """Grounded knowledge citation from curated agricultural corpus."""
    source_id: str = Field(..., description="Unique document/entry identifier in knowledge base")
    title: str = Field(..., description="Source title or university/KVK package of practice")
    url: str | None = Field(default=None, description="External reference URL if available")
    published_date: str | None = Field(default=None, description="Publication or validation date (YYYY-MM-DD)")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Vector similarity / relevance score")
    snippet: str = Field(..., description="Exact cited text excerpt supporting the advice")


class Advisory(SpokenResponseMixin):
    """Grounded 5-Point Advisory output structure."""
    id: str = Field(..., description="UUID string of the advisory record")
    farm_id: str = Field(..., description="UUID string of the target farm")
    
    # 5-Point Core Fields
    diagnosis: str = Field(..., description="Point 1: Identified disease, pest, or physiological condition")
    cause: str = Field(..., description="Point 2: Underlying causal agent, environmental driver, or pathogen")
    immediate_action: str = Field(..., description="Point 3: Prescribed immediate remediation or cultural control")
    preventative_action: str = Field(..., description="Point 4: Long-term preventative measures and field hygiene")
    recommended_inputs: list[str] = Field(
        default_factory=list,
        description="Point 5: Recommended organic or chemical inputs with exact dosage specifications",
    )

    citations: list[Citation] = Field(
        default_factory=list,
        description="Grounded citations from verified research sources",
    )
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Overall RAG grounding confidence score")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="ISO 8601 UTC creation timestamp")


class AdvisoryGenerateRequest(BaseModel):
    """Request to generate a grounded advisory for a query or crop diagnosis."""
    farm_id: str = Field(..., description="UUID string of farm")
    query_text: str | None = Field(default=None, description="Spoken or typed farmer query")
    diagnosis_id: str | None = Field(default=None, description="Optional UUID string of verified crop diagnosis")
    audio_asset_id: str | None = Field(default=None, description="Optional voice audio asset ID")
