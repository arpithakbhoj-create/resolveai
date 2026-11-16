
import re

from models import AIRecommendation



UNSAFE_PATTERNS = [
    # Disable firewall
    r"\bdisabl(?:e|ing|ed)\b.{0,60}\bfirewalls?\b",
    r"\bfirewalls?\b.{0,60}\bdisabl(?:e|ing|ed)\b",

    # Turn off firewall
    r"\bturn\s+off\b.{0,60}\bfirewalls?\b",
    r"\bfirewalls?\b.{0,60}\bturn(?:ed|ing)?\s+off\b",

    # Disable antivirus
    r"\bdisabl(?:e|ing|ed)\b.{0,60}\bantivirus\b",
    r"\bantivirus\b.{0,60}\bdisabl(?:e|ing|ed)\b",

    # Delete backups
    r"\bdelet(?:e|ing|ed)\b.{0,60}\bbackups?\b",
    r"\bbackups?\b.{0,60}\bdelet(?:e|ing|ed)\b",
]



def validate_recommendation_safety(
    recommendation: AIRecommendation
) -> None:

    # Check actionable troubleshooting steps.
    # Do not automatically block quoted incident descriptions.
    steps_text = "\n".join(
        recommendation.troubleshooting_steps
    )

    for pattern in UNSAFE_PATTERNS:
        if re.search(
            pattern,
            steps_text,
            flags=re.IGNORECASE
        ):
            raise RuntimeError(
                "AI recommendation blocked by safety validation."
            )
