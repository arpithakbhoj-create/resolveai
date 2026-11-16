
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

# Incident priority levels
class IncidentPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


# Incident status values
class IncidentStatus(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


# Incident categories
class IncidentCategory(str, Enum):
    INFRASTRUCTURE = "Infrastructure"
    NETWORK = "Network"
    APPLICATION = "Application"
    SECURITY = "Security"
    DATABASE = "Database"
    OTHER = "Other"


# Fields required to create an incident
class IncidentCreate(BaseModel):
    title: str = Field(min_length=5, max_length=200)
    description: str = Field(min_length=10)
    category: IncidentCategory
    priority: IncidentPriority
    use_ml_suggestion: bool = False


# Full incident record returned by the API


# Full incident record returned by the API
class Incident(BaseModel):
    id: int
    title: str
    description: str
    category: IncidentCategory
    priority: IncidentPriority
    status: IncidentStatus = IncidentStatus.OPEN
    resolution_notes: str | None = None
    resolved_at: str | None = None





# Fields allowed when updating an incident
class IncidentUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=200
    )

    description: Optional[str] = Field(
        default=None,
        min_length=10
    )

    category: Optional[IncidentCategory] = None

    priority: Optional[IncidentPriority] = None

    status: Optional[IncidentStatus] = None

    resolution_notes: Optional[str] = None


# INCIDENT HISTORY RESPONSE MODEL
class IncidentHistory(BaseModel):
    id: int
    incident_id: int
    field_name: str
    old_value: str | None = None
    new_value: str | None = None
    changed_at: str

# ML PREDICTION REQUEST
class IncidentPredictionRequest(BaseModel):
    description: str = Field(min_length=10)


# ML PREDICTION RESPONSE
class IncidentPredictionResponse(BaseModel):
    predicted_category: IncidentCategory
    confidence: float
    model_version: str


# INCIDENT CREATION RESPONSE WITH OPTIONAL ML SUGGESTION
class IncidentCreationResponse(BaseModel):
    incident: Incident
    ml_suggestion: IncidentPredictionResponse | None = None


class SimilarIncidentRequest(BaseModel):
    description: str = Field(min_length=10)
    top_k: int = Field(default=3, ge=1, le=10)


class AIRecommendation(BaseModel):
    incident_assessment: str = Field(min_length=1)
    troubleshooting_steps: list[str] = Field(
        min_length=3,
        max_length=5
    )
    historical_evidence: str = Field(min_length=1)
    limitations: str = Field(min_length=1)


class RAGResolutionResponse(BaseModel):
    recommendation_available: bool
    message: str
    ai_recommendation: AIRecommendation | None = None
    source_incidents: list[dict] = Field(
        default_factory=list
    )

