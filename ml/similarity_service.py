
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from service import get_resolved_incidents_service


# FIND SIMILAR HISTORICAL INCIDENTS
def find_similar_incidents(
    description: str,
    top_k: int = 3
):

    # Retrieve incidents with documented resolutions
    resolved_incidents = get_resolved_incidents_service()

    if not resolved_incidents:
        return []

    # Combine title and description for better matching
    historical_texts = [
        f"{incident.title} {incident.description}"
        for incident in resolved_incidents
    ]

    # Include the new incident in the comparison
    all_texts = historical_texts + [description]

    # Convert text into TF-IDF numerical vectors
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # The last vector represents the new incident
    new_incident_vector = tfidf_matrix[-1]

    # All earlier vectors represent historical incidents
    historical_vectors = tfidf_matrix[:-1]

    # Calculate cosine similarity scores
    similarity_scores = cosine_similarity(
        new_incident_vector,
        historical_vectors
    )[0]

    # Sort incidents from most similar to least similar
    ranked_indices = similarity_scores.argsort()[::-1]

    
    results = []

    for index in ranked_indices:

        score = float(similarity_scores[index])

        # Ignore incidents below the similarity threshold
        if score < 0.20:
            continue

        # Stop after collecting the requested number
        if len(results) >= top_k:
            break

        incident = resolved_incidents[index]

        results.append({
            "incident_id": incident.id,
            "title": incident.title,
            "description": incident.description,
            "category": incident.category.value,
            "similarity_score": round(score, 4),
            "resolution_notes": incident.resolution_notes
        })

    return results
