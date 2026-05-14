from datetime import datetime
from typing import TypedDict


class FeedbackDocument(TypedDict):
    user_id: str
    analysis_id: str
    agree_with_result: bool
    comment: str
    status: str
    created_at: datetime
