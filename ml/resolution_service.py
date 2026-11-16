
from ml.similarity_service import find_similar_incidents


def recommend_resolution(description: str):

    similar_incidents = find_similar_incidents(
        description=description,
        top_k=3
    )

    # No relevant historical incidents found
    if not similar_incidents:
        return {
            "recommendation_available": False,
            "message": (
                "No sufficiently similar resolved incidents "
                "were found. Manual investigation is required."
            ),
            "suggested_resolution": None,
            "source_incident_id": None,
            "similarity_score": None
        }

    # Select the highest-ranked historical incident
    best_match = similar_incidents[0]

    return {
        "recommendation_available": True,
        "message": (
            "A potentially relevant historical resolution "
            "was found. Review before applying."
        ),
        "suggested_resolution": best_match["resolution_notes"],
        "source_incident_id": best_match["incident_id"],
        "similarity_score": best_match["similarity_score"]
    }
