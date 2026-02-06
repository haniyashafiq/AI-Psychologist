"""API routes for NLP service"""
from fastapi import APIRouter, HTTPException, Depends
from app.api.schemas import (
    AnalysisRequest, 
    AnalysisResponse, 
    HealthResponse
)
from app.services.symptom_extractor import SymptomExtractor
from app.utils.logger import setup_logger
import time

logger = setup_logger(__name__)
router = APIRouter()

# Global state (will be initialized in main.py)
symptom_extractor: SymptomExtractor = None


def get_symptom_extractor():
    """Dependency to get symptom extractor instance"""
    if symptom_extractor is None:
        raise HTTPException(status_code=503, detail="Service not fully initialized")
    return symptom_extractor


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    from app.config.settings import settings
    
    return HealthResponse(
        status="healthy",
        service="nlp-service",
        version="1.0.0",
        spacy_model=settings.spacy_model,
        spacy_model_loaded=symptom_extractor is not None
    )


@router.post("/nlp/extract-symptoms", response_model=AnalysisResponse)
async def extract_symptoms(
    request: AnalysisRequest,
    extractor: SymptomExtractor = Depends(get_symptom_extractor)
):
    """
    Extract depression symptoms from natural language text
    
    Args:
        request: Analysis request with text to analyze
        
    Returns:
        Extracted symptoms with metadata
    """
    try:
        start_time = time.time()
        
        logger.info(f"Analyzing text of length {len(request.text)}")
        
        # Extract symptoms
        result = extractor.extract(request.text)
        
        # Add processing time
        processing_time_ms = (time.time() - start_time) * 1000
        result["metadata"]["processing_time_ms"] = round(processing_time_ms, 2)
        
        # Generate summary
        summary = extractor.get_symptom_summary(result)
        
        logger.info(
            f"Extracted {summary['unique_symptoms']} unique symptoms "
            f"in {processing_time_ms:.2f}ms"
        )
        
        return AnalysisResponse(
            success=True,
            data={
                "symptoms": result["symptoms"],
                "metadata": result["metadata"],
                "summary": summary
            }
        )
        
    except Exception as e:
        logger.error(f"Error during symptom extraction: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing text: {str(e)}"
        )
