from datetime import datetime
from typing import TypedDict


class SourceDocument(TypedDict):
    source_name: str
    topic: str
    source_url: str
    trust_score: float
    evidence_text: str
    keywords: list[str]
    source_type: str
    last_verified_at: datetime
