"""Pydantic schemas for API request/response validation"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any


class PreprocessingOptions(BaseModel):
    """Text preprocessing options"""
    remove_punctuation: bool = False
    lowercase: bool = False
    lemmatize: bool = True


class AnalysisContext(BaseModel):
    """Context for text analysis"""
    language: str = "en"
    preprocessing_options: Optional[PreprocessingOptions] = PreprocessingOptions()


class AnalysisRequest(BaseModel):
    """Request for symptom extraction"""
    text: str = Field(..., min_length=10, max_length=5000, description="Patient symptom description")
    context: Optional[AnalysisContext] = AnalysisContext()


class SymptomResponse(BaseModel):
    """Individual symptom detection result"""
    symptom_id: str
    dsm5_code: str
    name: str
    detected: bool
    confidence: float
    matched_phrases: List[str]
    sentence_context: Optional[str]
    is_negated: bool
    match_type: str


class AnalysisMetadata(BaseModel):
    """Metadata about the analysis"""
    tokens_count: int
    sentences_count: int
    temporal_markers: Dict[str, List[str]]
    intensity_markers: Dict[str, List[str]]
    functional_impairment: Dict[str, Any]
    duration_days: int
    processing_time_ms: Optional[float] = None


class AnalysisResponse(BaseModel):
    """Response from symptom extraction"""
    success: bool
    data: Dict[str, Any]
    message: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str
    spacy_model: str
    spacy_model_loaded: bool
