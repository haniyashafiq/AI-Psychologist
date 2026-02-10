"""Pydantic schemas for RAG service API request/response validation"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any


# --- Request Models ---

class SymptomInput(BaseModel):
    """Symptom data from the NLP service"""
    dsm5Code: str = ""
    symptomId: str = ""
    name: str = ""
    detected: bool = False
    confidence: float = 0.0
    evidence: List[str] = []
    sentenceContext: Optional[str] = None
    matchType: Optional[str] = None


class AssessmentMetadata(BaseModel):
    """Additional metadata from the backend"""
    durationDays: Optional[int] = None
    durationSpecified: Optional[bool] = None
    functionalImpairment: Optional[Any] = None
    processingTime: Optional[float] = None


class RAGQueryRequest(BaseModel):
    """Request to perform RAG-powered clinical assessment"""
    text: str = Field(..., min_length=10, max_length=10000, description="Patient presentation text")
    symptoms: Optional[List[SymptomInput]] = None
    metadata: Optional[AssessmentMetadata] = None
    disorder_filter: Optional[str] = Field(
        None,
        description="Optional disorder code to filter retrieval (e.g., 'F32' for MDD)"
    )


# --- Response Models ---

class DSMReference(BaseModel):
    """A DSM-5-TR reference cited in the assessment"""
    criteria_code: str = ""
    criteria_text: str = ""
    relevance: str = ""
    evidence_strength: str = ""


class DifferentialConsideration(BaseModel):
    """A differential diagnosis to consider"""
    condition: str = ""
    dsm5_code: str = ""
    rationale: str = ""
    distinguishing_features: str = ""


class RecommendedAssessment(BaseModel):
    """A recommended assessment instrument"""
    instrument: str = ""
    purpose: str = ""


class ClinicalAssessment(BaseModel):
    """The LLM-generated clinical assessment"""
    clinical_narrative: str = ""
    dsm_references: List[DSMReference] = []
    differential_considerations: List[DifferentialConsideration] = []
    severity_rationale: str = ""
    recommended_assessments: List[RecommendedAssessment] = []
    risk_factors: List[str] = []
    protective_factors: List[str] = []
    confidence_notes: str = ""


class SourceReference(BaseModel):
    """A source chunk from the vector database"""
    section: str = ""
    disorder: str = ""
    code: str = ""
    pages: str = ""
    type: str = ""
    relevance_score: float = 0.0
    excerpt: str = ""


class PipelineMetrics(BaseModel):
    """Performance metrics for the RAG pipeline"""
    embedding_ms: float = 0.0
    retrieval_ms: float = 0.0
    llm_ms: float = 0.0
    total_ms: float = 0.0
    chunks_retrieved: int = 0


class TokenUsage(BaseModel):
    """Token usage from the LLM call"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    model: str = ""


class RAGQueryResponse(BaseModel):
    """Full RAG assessment response"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str
    openai_model: str
    embedding_model: str
    chromadb_status: str
    document_count: int
