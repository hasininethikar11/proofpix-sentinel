from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from .analyzer import analyze_url
from .schemas import AnalyzeRequest, AnalyzeResponse

app = FastAPI(title="PROOFPIX SENTINEL API", version="0.1.0",
              description="Local heuristic URL analysis prototype; not a guarantee of safety.")

# The extension calls this API from a chrome-extension:// origin. Restrict CORS to
# extension origins; localhost health/API calls from tools do not need browser CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^chrome-extension://[a-p]{32}$",
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "PROOFPIX SENTINEL API", "mode": "offline-heuristics"}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    try:
        result = analyze_url(request.url)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return AnalyzeResponse(**result)
