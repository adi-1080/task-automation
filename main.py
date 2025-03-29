from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from gemini_client import analyze_tasks_with_budget
from poster_service import generate_posters
from schemas import TaskRequest, TaskResponse
from schemas import PosterRequest, PosterResponse
import uvicorn

app = FastAPI(title="AI Task & Budget Manager")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/analyze-task", response_model=TaskResponse)
async def analyze_task(request: TaskRequest):
    """
    Endpoint that:
    - Breaks down tasks
    - Assigns to departments
    - Provides budget estimates
    """
    try:
        result = analyze_tasks_with_budget(
            task=request.task,
            departments=request.departments,
            currency=request.currency
        )
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
            
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Task analysis failed: {str(e)}"
        )
        
@app.post("/generate-posters", response_model=PosterResponse)
async def create_posters(request: PosterRequest):
    try:
        print("Received data:", request.dict())
        result = generate_posters(request.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)