from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List
import importlib
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Secure Code Quality Evaluator",
    description="API for evaluating AI-generated code quality",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize evaluators
evaluators = {
    "correctness": "app.evaluators.correctness_evaluator:CorrectnessEvaluator",
    "maintainability": "app.evaluators.maintainability_evaluator:MaintainabilityEvaluator",
    "security": "app.evaluators.security_evaluator:SecurityEvaluator"
}

# Initialize evaluator instances
evaluator_instances = {}
for name, path in evaluators.items():
    try:
        module_path, class_name = path.split(':')
        module = importlib.import_module(module_path)
        evaluator_class = getattr(module, class_name)
        evaluator_instances[name] = evaluator_class()
        logger.info(f"Successfully initialized evaluator: {name}")
    except Exception as e:
        logger.error(f"Failed to initialize evaluator {name}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to initialize evaluator {name}: {str(e)}"
        )

class CodeEvaluationRequest(BaseModel):
    code: str
    evaluators: List[str] = ["correctness", "maintainability", "security"]

class CodeEvaluationResponse(BaseModel):
    results: Dict[str, Any]
    overall_score: float
    timestamp: str

@app.post("/evaluate", response_model=CodeEvaluationResponse)
async def evaluate_code(request: CodeEvaluationRequest):
    """
    Evaluate code using specified evaluators.
    Returns a comprehensive report including individual evaluator results
    and an overall score.
    """
    try:
        logger.debug(f"Received evaluation request for code: {request.code[:100]}...")
        
        if not request.code:
            raise HTTPException(status_code=400, detail="Code cannot be empty")
        
        results = {}
        scores = []
        
        for evaluator_name in request.evaluators:
            if evaluator_name not in evaluator_instances:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unknown evaluator: {evaluator_name}"
                )
            
            logger.debug(f"Evaluating with {evaluator_name}...")
            evaluator = evaluator_instances[evaluator_name]
            result = evaluator.evaluate(request.code)
            results[evaluator_name] = result
            
            # Calculate score based on evaluator type
            if evaluator_name == "correctness":
                scores.append(100 if result["results"]["results"]["pep8_compliance"] else 0)
            elif evaluator_name == "maintainability":
                scores.append(result["results"]["results"]["maintainability_index"])
            elif evaluator_name == "security":
                scores.append(result["results"]["results"]["security_score"])
        
        # Calculate overall score as weighted average
        overall_score = sum(scores) / len(scores) if scores else 0
        
        response = {
            "results": {k: v["results"] for k, v in results.items()},
            "overall_score": overall_score,
            "timestamp": datetime.now().isoformat()
        }
        logger.debug(f"Evaluation complete. Response: {json.dumps(response, indent=2)}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error during evaluation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error during evaluation: {str(e)}"
        )

@app.get("/")
async def root():
    return {"message": "Welcome to Secure Code Quality Evaluator API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
