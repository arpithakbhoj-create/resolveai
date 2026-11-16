
import agent.incident_graph as graph_module


def test_graph_routes_to_ai_recommendation(monkeypatch):

    # Mock the ML classifier
    monkeypatch.setattr(
        graph_module,
        "predict_incident_category",
        lambda description: {
            "predicted_category": "Database",
            "confidence": 0.90,
            "model_version": "test"
        }
    )

    # Mock historical retrieval
    monkeypatch.setattr(
        graph_module,
        "find_similar_incidents",
        lambda description, top_k=3: [
            {
                "incident_id": 1,
                "title": "SQL Server connectivity failure",
                "description": description,
                "category": "Database",
                "similarity_score": 0.80,
                "resolution_notes": "Network configuration corrected."
            }
        ]
    )

    # Mock the RAG service
    monkeypatch.setattr(
        graph_module,
        "generate_rag_resolution",
        lambda description, similar_incidents: {
            "recommendation_available": True,
            "ai_recommendation": {
                "incident_assessment": "Database connectivity issue"
            },
            "source_incidents": [
                {"incident_id": 1}
            ]
        }
    )

    result = graph_module.incident_graph.invoke({
        "description": "Application cannot connect to SQL Server."
    })

    assert result["status"] == (
        "AI recommendation generated. Human review required."
    )

    assert result["recommendation"]["recommendation_available"] is True


def test_graph_routes_to_manual_investigation(monkeypatch):

    # Mock the ML classifier
    monkeypatch.setattr(
        graph_module,
        "predict_incident_category",
        lambda description: {
            "predicted_category": "Other",
            "confidence": 0.50,
            "model_version": "test"
        }
    )

    # Mock retrieval with no historical matches
    monkeypatch.setattr(
        graph_module,
        "find_similar_incidents",
        lambda description, top_k=3: []
    )

    # Track whether the RAG service gets called
    rag_called = []

    def fake_rag(description, similar_incidents):
        rag_called.append(True)
        return {}

    monkeypatch.setattr(
        graph_module,
        "generate_rag_resolution",
        fake_rag
    )

    result = graph_module.incident_graph.invoke({
        "description": "Office printer is producing blank pages."
    })

    assert result["status"] == (
        "No historical evidence found. Manual investigation required."
    )

    assert "recommendation" not in result
    assert rag_called == []
