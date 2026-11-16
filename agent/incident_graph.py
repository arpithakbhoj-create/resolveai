
from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from ml.model_service import predict_incident_category
from ml.similarity_service import find_similar_incidents
from ml.rag_service import generate_rag_resolution


# 1. Define the graph state
class IncidentState(TypedDict, total=False):
    description: str
    predicted_category: Any
    similar_incidents: list
    recommendation: Any
    status: str


# 2. Classify the incident
def classify_incident(state: IncidentState):
    description = state["description"]

    prediction = predict_incident_category(description)

    return {
        "predicted_category": prediction
    }


# 3. Retrieve historical incidents
def retrieve_historical_incidents(state: IncidentState):
    description = state["description"]

    similar_incidents = find_similar_incidents(
        description,
        top_k=3
    )

    return {
        "similar_incidents": similar_incidents
    }


# 4. Decide the next step
def decide_next_step(state: IncidentState):
    similar_incidents = state.get("similar_incidents", [])

    if similar_incidents:
        return "evidence_found"

    return "no_evidence"


# 5. Handle available historical evidence
# Handle available historical evidence and generate AI guidance
def handle_evidence_found(state: IncidentState):

    recommendation = generate_rag_resolution(
        description=state["description"],
        similar_incidents=state["similar_incidents"]
    )

    return {
        "recommendation": recommendation,
        "status": "AI recommendation generated. Human review required."
    }


# 6. Handle missing historical evidence
def handle_no_evidence(state: IncidentState):
    return {
        "status": "No historical evidence found. Manual investigation required."
    }


# 7. Build the LangGraph workflow
graph_builder = StateGraph(IncidentState)

# Register nodes
graph_builder.add_node("classify", classify_incident)
graph_builder.add_node("retrieve", retrieve_historical_incidents)
graph_builder.add_node("evidence_found", handle_evidence_found)
graph_builder.add_node("no_evidence", handle_no_evidence)

# Define execution order
graph_builder.add_edge(START, "classify")
graph_builder.add_edge("classify", "retrieve")

# Define conditional routing
graph_builder.add_conditional_edges(
    "retrieve",
    decide_next_step,
    {
        "evidence_found": "evidence_found",
        "no_evidence": "no_evidence"
    }
)

graph_builder.add_edge("evidence_found", END)
graph_builder.add_edge("no_evidence", END)


# 8. Compile the graph
incident_graph = graph_builder.compile()


# 9. Test the workflow
if __name__ == "__main__":
    result = incident_graph.invoke({
        "description": "The office printer is producing blank pages and showing a paper sensor warning."
    })

    print("\n--- ResolveAI LangGraph Output ---")
    print("Incident:", result["description"])
    print("Predicted category:", result["predicted_category"])
    print("Similar incidents:", result["similar_incidents"])
    print("Workflow status:", result["status"])


    print("\n--- AI Recommendation ---")

    recommendation = result.get("recommendation")

    if recommendation:
      print("Assessment:", recommendation["ai_recommendation"]["incident_assessment"])

      print("\nTroubleshooting steps:")
      for step in recommendation["ai_recommendation"]["troubleshooting_steps"]:
        print("-", step)

      print("\nHistorical evidence:")
      print(recommendation["ai_recommendation"]["historical_evidence"])

      print("\nLimitations:")
      print(recommendation["ai_recommendation"]["limitations"])

      print("\nSource incidents:")
      print(recommendation["source_incidents"])
    else:
      print("No AI recommendation generated.")