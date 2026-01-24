from fastapi import FastAPI
from pydantic import BaseModel
from app import run_orchestrator

app = FastAPI(title="Research Summarization API")

class ResearchRequest(BaseModel):
    topic: str

@app.post("/research")
async def research_pipeline(request: ResearchRequest):
    result = run_orchestrator(request.topic)
    return result
