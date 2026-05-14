# VerifyIT Backend

FastAPI backend for the VerifyIT AI-driven IT Educational Claim Credibility Analyzer.

## Stack

- Python 3.11+
- FastAPI
- MongoDB Atlas
- Motor async MongoDB driver
- Pydantic v2
- JWT Bearer authentication
- bcrypt password hashing
- Ollama Cloud adapter for normalization, internal verification, explanations, summaries, and follow-up questions

## Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Fill `.env`:

```env
MONGODB_URI=mongodb+srv://...
MONGODB_DB_NAME=verifyit
JWT_SECRET_KEY=replace-with-a-long-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
FRONTEND_ORIGIN=http://localhost:5173,http://127.0.0.1:5173
OLLAMA_API_KEY=
OLLAMA_BASE_URL=https://api.ollama.com
OLLAMA_MODEL=deepseek-v4-flash:cloud
```

Run:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The app creates indexes and seeds trusted sources on startup when the `sources` collection is empty.

## API Examples

Health:

```http
GET /api/health
```

Signup:

```http
POST /api/auth/signup
Content-Type: application/json

{
  "full_name": "Test Analyst",
  "email": "analyst@example.com",
  "password": "Password123"
}
```

Login:

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "analyst@example.com",
  "password": "Password123"
}
```

Analyze claim:

```http
POST /api/claims/analyze
Authorization: Bearer <token>
Content-Type: application/json

{
  "claim": "RAM stores files permanently.",
  "selected_topic": "Hardware"
}
```

Example response:

```json
{
  "status": "completed",
  "analysis_id": "662d...",
  "claim_id": "662d...",
  "claim": "RAM stores files permanently.",
  "normalized_claim": "ram stores files permanently",
  "topic": "Hardware",
  "verdict": "Misleading",
  "confidence": 87,
  "explanation": "The claim appears misleading because trusted evidence from Microsoft Learn contradicts or limits the statement...",
  "evidence_summary": "RAM is volatile memory used by running programs...",
  "feature_scores": {
    "source_trust_score": 0.96,
    "similarity_score": 0.42,
    "entailment_score": 0.18,
    "contradiction_score": 0.82,
    "neutral_score": 0.18,
    "source_agreement_score": 0.72,
    "evidence_coverage_score": 0.66
  },
  "sources": [
    {
      "id": "662d...",
      "source_name": "Microsoft Learn",
      "topic": "Hardware",
      "source_url": "https://learn.microsoft.com/",
      "trust_score": 0.96,
      "evidence_text": "RAM is volatile memory used by running programs...",
      "source_type": "Official Documentation",
      "match_score": 0.74,
      "last_verified_at": "2026-04-26T00:00:00Z"
    }
  ],
  "suggested_questions": [
    "Can you explain the evidence in simpler terms?",
    "Which source supports this result?",
    "Why is this claim considered misleading?",
    "What is the correct concept?"
  ],
  "followup_questions": [
    "Why is this claim considered misleading?",
    "What is the correct concept?",
    "Which source supports this result?"
  ],
  "model_used": "VerifyIT hybrid verification pipeline",
  "created_at": "2026-04-26T00:00:00Z"
}
```

Out-of-scope claims return HTTP 200 and are not stored as completed analyses:

```json
{
  "status": "out_of_scope",
  "message": "This claim is outside VerifyIT's scope. VerifyIT only analyzes Computer Science and IT educational claims.",
  "detected_domain": "Health",
  "confidence": 91,
  "reason": "The claim appears to be about health, not Computer Science or IT education.",
  "suggested_claims": [
    "RAM stores data permanently.",
    "HTML is a programming language.",
    "DNS converts domain names to IP addresses.",
    "A primary key uniquely identifies a row in a database."
  ]
}
```

Other protected endpoints:

```http
GET /api/auth/me
POST /api/auth/logout
GET /api/claims/history?search=ram&verdict=Misleading&topic=Hardware&page=1&page_size=20
GET /api/claims/{analysis_id}
DELETE /api/claims/{analysis_id}
GET /api/sources
GET /api/sources?topic=Web%20Development
GET /api/sources/{source_id}
POST /api/feedback
GET /api/settings
PUT /api/settings
```

## Frontend Integration

Create `frontend/.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

Start frontend:

```powershell
cd frontend
npm.cmd run dev -- --host 127.0.0.1 --port 5173
```

## Design Notes

- VerifyIT uses a hybrid pipeline: domain validation, evidence retrieval, feature extraction, trained/placeholder ML prediction, LLM-assisted verification, consensus decision logic, and evidence-grounded explanation.
- Computer Science / IT scope validation runs before retrieval and classification.
- Out-of-scope claims are stored separately in `rejected_claims`, not in completed analysis history.
- Ollama Cloud calls are optional at runtime. If the LLM call fails, deterministic fallbacks keep the API usable.
- The public verdict is the final VerifyIT verification result, not a raw ML-only result.
- Raw ML prediction, LLM verification, decision source, and internal reasoning are stored under `analysis_debug` for audit/debugging and are not exposed to standard users.
- The explanation service only explains the final consensus verdict using retrieved evidence.
- A trained model can later replace `predict_credibility(features, claim, evidence_list)` without changing API contracts.
