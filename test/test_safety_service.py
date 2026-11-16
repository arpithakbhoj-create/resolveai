
import pytest

from models import AIRecommendation
from ml.safety_service import validate_recommendation_safety


def create_recommendation(steps):
    return AIRecommendation(
        incident_assessment="SQL Server connectivity issue",
        troubleshooting_steps=steps,
        historical_evidence="Historical incident #1",
        limitations="Requires further investigation."
    )


def test_blocks_firewall_disabling():
    recommendation = create_recommendation([
        "Verify that the SQL Server firewall is disabled.",
        "Check database connectivity.",
        "Review application logs."
    ])

    with pytest.raises(RuntimeError):
        validate_recommendation_safety(recommendation)


def test_blocks_direct_firewall_instruction():
    recommendation = create_recommendation([
        "Disable the firewall immediately.",
        "Check database connectivity.",
        "Review application logs."
    ])

    with pytest.raises(RuntimeError):
        validate_recommendation_safety(recommendation)


def test_allows_safe_troubleshooting():
    recommendation = create_recommendation([
        "Verify that SQL Server is running.",
        "Check network connectivity.",
        "Review application error logs."
    ])

    validate_recommendation_safety(recommendation)
