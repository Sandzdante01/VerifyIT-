from datetime import datetime
from typing import Any, TypedDict


class ClaimDocument(TypedDict):
    user_id: str
    claim: str
    normalized_claim: str
    topic: str
    created_at: datetime


class AnalysisDocument(TypedDict):
    user_id: str
    claim_id: str
    claim: str
    normalized_claim: str
    topic: str
    verdict: str
    confidence: int
    explanation: str
    evidence_summary: str
    feature_scores: dict[str, float]
    sources: list[dict[str, Any]]
    suggested_questions: list[str]
    followup_questions: list[str]
    model_used: str
    analysis_debug: dict[str, Any]
    created_at: datetime
