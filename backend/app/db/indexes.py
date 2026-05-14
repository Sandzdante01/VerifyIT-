from pymongo import ASCENDING, DESCENDING

from app.db.mongodb import get_database


async def create_indexes() -> None:
    db = get_database()
    await db.users.create_index([("email", ASCENDING)], unique=True)
    await db.analyses.create_index([("user_id", ASCENDING)])
    await db.analyses.create_index([("created_at", DESCENDING)])
    await db.sources.create_index([("topic", ASCENDING)])
    await db.sources.create_index([("source_name", ASCENDING), ("topic", ASCENDING)])
    await db.claims.create_index([("normalized_claim", ASCENDING)])
    await db.rejected_claims.create_index([("user_id", ASCENDING)])
    await db.rejected_claims.create_index([("created_at", DESCENDING)])
