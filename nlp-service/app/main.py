"""FastAPI application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import spacy
from app.api import routes
from app.services.symptom_extractor import SymptomExtractor
from app.config.settings import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle event handler for startup and shutdown"""
    # Startup
    logger.info("Starting NLP service...")
    logger.info(f"Loading spaCy model: {settings.spacy_model}")
    
    try:
        nlp_model = spacy.load(settings.spacy_model)
        logger.info(f"Successfully loaded spaCy model: {settings.spacy_model}")
        
        # Initialize symptom extractor
        routes.symptom_extractor = SymptomExtractor(nlp_model)
        logger.info("Symptom extractor initialized")
        
    except OSError as e:
        logger.error(
            f"Failed to load spaCy model '{settings.spacy_model}'. "
            f"Please run: python -m spacy download {settings.spacy_model}"
        )
        raise
    
    logger.info(f"NLP service started on {settings.host}:{settings.port}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down NLP service...")


# Create FastAPI app
app = FastAPI(
    title="Depression Diagnosis NLP Service",
    description="Natural language processing service for extracting depression symptoms from text",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
if settings.enable_cors:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routes
app.include_router(routes.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "nlp-service",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "extract_symptoms": "/nlp/extract-symptoms"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=settings.log_level.lower()
    )
