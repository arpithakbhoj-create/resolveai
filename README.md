ResolveAI – AI-Powered IT Incident Management API
ResolveAI is a portfolio project that demonstrates how machine learning, retrieval-augmented generation (RAG), and workflow orchestration can support IT incident management.

The application exposes a REST API built with FastAPI. It stores incident records in SQLite, uses a scikit-learn text-classification model to suggest incident categories, and includes components for similarity-based retrieval, resolution assistance, and an LLM-powered workflow.
Project status: Portfolio/demo implementation. It is not a production incident-management platform. The Azure deployment has been validated for API access and basic incident creation/retrieval. Cloud database persistence and cloud-hosted LLM/RAG execution are not currently implemented.

Features
- Create, retrieve, and update IT incidents through REST API endpoints.
- Store incident records using SQLite.
- Suggest an incident category using a TF-IDF and scikit-learn classification pipeline.
- Return the model's predicted category, confidence score, and model version with incident creation.
- Include supporting components for similarity search and resolution assistance.
- Define an incident-handling workflow using LangGraph.
- Include a basic input safety filter.
- Run automated tests with pytest.
- Build a Docker image and run CI checks using GitHub Actions.
- Deploy the API container to Azure Container Apps using Azure Container Registry.
Technology stack
Area	Technologies
API	Python, FastAPI, Uvicorn, Pydantic
Machine learning	scikit-learn, TF-IDF, joblib, pandas
LLM / workflow components	Ollama, Qwen, RAG components, LangGraph
Database	SQLite
Testing	pytest
Containerization	Docker, Docker Compose
CI	GitHub Actions
Cloud deployment	Azure Container Registry (ACR), Azure Container Apps (ACA), managed identity


High-level architecture
                  Client / Swagger UI
                          |
                          v
                    FastAPI API
                          |
             +------------+------------+
             |            |            |
             v            v            v
        Incident       ML category   Incident
        service        prediction    database
             |         (TF-IDF +     (SQLite)
             |         classifier)
             |
             v
      AI assistance components
       - Similarity retrieval
       - Resolution assistance
       - RAG service
       - Ollama / Qwen integration
       - LangGraph workflow
       - Basic safety filtering
The API and incident CRUD flow are available in the Azure deployment. The Ollama/Qwen LLM runtime is not hosted in Azure as part of the current deployment, so cloud-hosted LLM/RAG execution should not be assumed.
Repository structure
resolveai/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   ├── generate_dataset.py
│   ├── incidents.csv
│   └── evaluation.csv
├── ml/
│   ├── train_model.py
│   ├── predict.py
│   ├── evaluate_model.py
│   ├── model_service.py
│   ├── similarity_service.py
│   ├── resolution_service.py
│   ├── ollama_service.py
│   ├── rag_service.py
│   ├── safety_service.py
│   └── incident_classifier.joblib
├── agent/
│   └── incident_graph.py
├── test/
│   ├── test_safety_service.py
│   └── test_incident_graph.py
├── main.py
├── models.py
├── service.py
├── database.py
├── requirements.txt
├── Dockerfile
└── compose.yaml
The trained model artifact may be generated during setup/build rather than committed to source control, depending on the repository's current .gitignore configuration.
Getting started locally
Prerequisites
- Python 3.14
- Git
- Docker Desktop (optional, for container-based execution)
1. Clone the repository
git clone https://github.com/arpithakbhoj-create/resolveai.git
cd resolveai
2. Create and activate a virtual environment
macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate
Windows PowerShell:
python -m venv .venv
.venv\Scripts\Activate.ps1
3. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
4. Train the incident classification model
python ml/train_model.py
This trains the text-classification model using the project dataset.
5. Start the API
uvicorn main:app --reload
Open the interactive API documentation:
- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI schema: http://127.0.0.1:8000/openapi.json
API overview
The currently validated incident operations are:
Method	Endpoint	Purpose
POST	/incidents	Create an incident; the request can ask the API to provide an ML category suggestion.
GET	/incidents	Retrieve incident records.
PATCH	/incidents/{incident_id}	Update selected incident fields, including status and resolution notes.


Use Swagger UI at /docs to inspect the current request schemas and try the endpoints. The exact fields accepted by each endpoint are defined by the API's Pydantic models.
Example: create an incident
curl -X POST "http://127.0.0.1:8000/incidents" \
  -H "Content-Type: application/json" \
  -H "accept: application/json" \
  -d '{
    "title": "Database connectivity issue",
    "description": "The application is unable to connect to the database server and users are experiencing request failures.",
    "category": "Database",
    "priority": "High",
    "use_ml_suggestion": true
  }'
When ML suggestion is enabled, the response includes the incident record and an ML suggestion containing the predicted category, confidence, and model version.
Example: retrieve incidents
curl -X GET "http://127.0.0.1:8000/incidents" \
  -H "accept: application/json"
Machine learning approach
The project includes a text classification pipeline based on TF-IDF features and a scikit-learn classifier. It uses incident text to predict a category.

The repository contains a synthetic incident dataset and a separate evaluation dataset. The current dataset is small and intended for demonstration and experimentation, not for drawing production-level conclusions.

Important: A predicted category is a suggestion, not a guaranteed classification. During Azure API validation, the model returned the correct category for a sample incident, but its confidence was approximately 0.25. This is a low confidence score and should not be represented as a highly reliable prediction. Model performance should be assessed using the evaluation script and appropriate metrics before making stronger claims.

Run model evaluation with:
python ml/evaluate_model.py
Running tests
Install the project dependencies, train the model if required by the test setup, and run:
python -m pytest test/ -v
The project has a small automated test suite. The LangGraph workflow tests use mocks for LLM/retrieval dependencies; they do not demonstrate a live end-to-end LLM integration. Five tests passed during the recorded local validation.
Run with Docker
Build the image:
docker build -t resolveai:1.0 .
Run the container:
docker run --rm -p 8000:8000 resolveai:1.0
Then open http://localhost:8000/docs.

To use the repository's Docker Compose configuration:
docker compose up --build
Stop the services:
docker compose down
Whether data persists after a container is removed depends on the volume configuration in compose.yaml. Removing named volumes with docker compose down -v deletes those volumes.
CI and Azure deployment
The GitHub Actions workflow in .github/workflows/ci.yml performs the following on pushes to main and pull requests targeting main:
1. Checks out the repository.
2. Sets up Python 3.14 and installs dependencies.
3. Trains the ML model.
4. Runs the pytest suite.
5. On pushes to main, authenticates to Azure.
6. Logs in to Azure Container Registry.
7. Builds and pushes a Linux AMD64 container image to ACR.
The workflow currently builds and pushes the image. Updating the running Azure Container App is a separate deployment step and is not automatically performed by this workflow.
Azure components used
- Azure Resource Group: rg-resolveai-dev
- Azure Container Registry: resolveaidev
- Azure Container Apps environment: cae-resolveai-dev
- Azure Container App: resolveai-app
- User-assigned managed identity: id-resolveai-acr
The Container App pulls its image from ACR using a managed identity. The deployed API is exposed through Azure Container Apps ingress.
Deployed API
- Swagger UI: https://resolveai-app.wonderfulbeach-263fec37.southindia.azurecontainerapps.io/docs
- Incidents endpoint: https://resolveai-app.wonderfulbeach-263fec37.southindia.azurecontainerapps.io/incidents
The deployed API was validated with successful incident creation (POST, HTTP 201) and retrieval (GET, HTTP 200). Updating an incident with PATCH had also been validated previously.
Current limitations and next improvements
- Cloud database persistence: The current Azure deployment uses /tmp/resolveai.db, which is temporary container storage. Data may be lost when the container is restarted or replaced. SQLite over the tested Azure Files SMB mount resulted in a database-locking error, so that mount is not used for the database. A managed database such as Azure Database for PostgreSQL would be a more suitable next step for durable cloud persistence.
- LLM/RAG hosting: Ollama/Qwen is not hosted in the current Azure deployment. The LLM and RAG components should be treated as local/development capabilities unless separately configured and deployed.
- Model confidence: The training dataset is small and synthetic. Predictions and confidence scores require further evaluation and improvement before any operational use.
- Safety filtering: The current safety filter uses basic pattern matching and is not a comprehensive prompt-injection or security defense.
- Test coverage: Workflow tests mock external LLM/retrieval behavior. More integration tests are needed for live model, retrieval, database, and deployed-cloud behavior.
- Production readiness: Authentication, authorization, secrets management, observability, durable storage, scalability testing, and stronger security controls would be needed before production use.
Data and security note
The included incident data is synthetic and intended for demonstration. Do not add employer-confidential, customer, personal, or otherwise sensitive incident data to this public portfolio repository.
License
No license has been specified yet. Add a license file if you intend to permit reuse or distribution of this project.