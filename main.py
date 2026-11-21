

from models import SimilarIncidentRequest

from ml.resolution_service import recommend_resolution

from ml.similarity_service import find_similar_incidents

from ml.rag_service import generate_rag_resolution


from models import (
    IncidentPredictionRequest,
    IncidentPredictionResponse
)

from ml.model_service import predict_incident_category

from fastapi import FastAPI, HTTPException, status
from contextlib import asynccontextmanager

from database import initialize_database

from models import Incident, IncidentCreate, IncidentUpdate, IncidentHistory, IncidentCreationResponse
from models import RAGResolutionResponse

from service import (
    create_incident_service,
    get_incidents_service,
    get_incident_by_id_service,
    update_incident_service,
    get_incident_history_service,
    get_incident_statistics_service
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Application startup
    initialize_database()

    yield

    # Application shutdown
    print("ResolveAI application shutting down")

app = FastAPI(
    title="ResolveAI",
    description="AI-powered IT Incident Intelligence and Resolution Assistant",
    version="1.0.0",
    lifespan=lifespan
)


# Home endpoint
@app.get("/")
def home():
    return {
        "application": "ResolveAI",
        "message": "Welcome to ResolveAI",
        "status": "running"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ResolveAI Backend"
    }


# Create an incident

# CREATE INCIDENT WITH OPTIONAL ML SUGGESTION
@app.post(
    "/incidents",
    response_model=IncidentCreationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_incident(incident: IncidentCreate):

    # Generate ML suggestion only when requested
    ml_suggestion = None

    if incident.use_ml_suggestion:
        ml_suggestion = predict_incident_category(
            incident.description
        )

    # Save the incident using the user's selected category
    created_incident = create_incident_service(incident)

    # Return both the incident and ML suggestion
    return {
        "incident": created_incident,
        "ml_suggestion": ml_suggestion
    }



# Retrieve all incidents
@app.get("/incidents", response_model=list[Incident])
def get_incidents():
    return get_incidents_service()

# GET INCIDENT STATISTICS
@app.get("/incidents/statistics")
def get_incident_statistics():

    return get_incident_statistics_service()



# SEARCH SIMILAR HISTORICAL INCIDENTS
@app.post("/incidents/similar")
def search_similar_incidents(
    request: SimilarIncidentRequest
):
    results = find_similar_incidents(
        description=request.description,
        top_k=request.top_k
    )

    return {
        "query": request.description,
        "total_matches": len(results),
        "similar_incidents": results
    }


# Retrieve a specific incident
@app.get("/incidents/{incident_id}", response_model=Incident)
def get_incident_by_id(incident_id: int):
    incident = get_incident_by_id_service(incident_id)

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident





# UPDATE AN EXISTING INCIDENT
@app.patch(
    "/incidents/{incident_id}",
    response_model=Incident
)
def update_incident(
    incident_id: int,
    incident_data: IncidentUpdate
):

    try:
        updated_incident = update_incident_service(
            incident_id,
            incident_data
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    if updated_incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return updated_incident


# GET INCIDENT CHANGE HISTORY
@app.get(
    "/incidents/{incident_id}/history",
    response_model=list[IncidentHistory]
)
def get_incident_history(incident_id: int):

    incident = get_incident_by_id_service(incident_id)

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return get_incident_history_service(incident_id)



# PREDICT INCIDENT CATEGORY USING ML
@app.post(
    "/predict-category",
    response_model=IncidentPredictionResponse
)
def predict_category(
    request: IncidentPredictionRequest
):

    prediction = predict_incident_category(
        request.description
    )

    return prediction




# RECOMMEND RESOLUTION BASED ON HISTORICAL INCIDENTS
@app.post("/incidents/recommend-resolution")
def get_resolution_recommendation(
    request: IncidentPredictionRequest
):

    recommendation = recommend_resolution(
        description=request.description
    )

    return recommendation


# GENERATE VALIDATED AI-POWERED INCIDENT RESOLUTION
@app.post(
    "/incidents/ai-resolution",
    response_model=RAGResolutionResponse
)
def generate_ai_resolution(
    request: IncidentPredictionRequest
):

    try:
        result = generate_rag_resolution(
            description=request.description
        )

        return result

    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="AI recommendation service is unavailable."
        )

