"""Text preprocessing utilities"""
import re
from typing import Dict, List
from unidecode import unidecode
from app.models.symptom_patterns import TEMPORAL_MARKERS, INTENSITY_MARKERS, FUNCTIONAL_IMPAIRMENT_KEYWORDS
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class TextProcessor:
    """Handles text preprocessing and basic NLP tasks"""
    
    def __init__(self):
        self.temporal_markers = TEMPORAL_MARKERS
        self.intensity_markers = INTENSITY_MARKERS
        self.impairment_keywords = FUNCTIONAL_IMPAIRMENT_KEYWORDS
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Convert to ASCII (handle unicode)
        text = unidecode(text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def extract_temporal_markers(self, text: str) -> Dict[str, List[str]]:
        """Extract temporal/duration markers from text"""
        text_lower = text.lower()
        found_markers = {
            "chronic": [],
            "frequent": [],
            "recent": [],
            "intermittent": []
        }
        
        for category, markers in self.temporal_markers.items():
            for marker in markers:
                if marker in text_lower:
                    found_markers[category].append(marker)
        
        return found_markers
    
    def extract_intensity_markers(self, text: str) -> Dict[str, List[str]]:
        """Extract intensity/severity markers from text"""
        text_lower = text.lower()
        found_markers = {
            "high": [],
            "moderate": [],
            "low": []
        }
        
        for category, markers in self.intensity_markers.items():
            for marker in markers:
                if marker in text_lower:
                    found_markers[category].append(marker)
        
        return found_markers
    
    def detect_functional_impairment(self, text: str) -> Dict[str, any]:
        """Detect functional impairment indicators in text"""
        text_lower = text.lower()
        detected_impairments = []
        
        for keyword in self.impairment_keywords:
            if keyword in text_lower:
                detected_impairments.append(keyword)
        
        has_impairment = len(detected_impairments) > 0
        severity = "none"
        
        if len(detected_impairments) >= 3:
            severity = "severe"
        elif len(detected_impairments) >= 2:
            severity = "moderate"
        elif len(detected_impairments) >= 1:
            severity = "mild"
        
        return {
            "detected": has_impairment,
            "severity": severity,
            "keywords": detected_impairments,
            "count": len(detected_impairments)
        }
    
    def extract_duration_days(self, text: str) -> int:
        """Extract duration in days from text"""
        text_lower = text.lower()
        duration_days = 0
        
        # Look for week patterns
        week_match = re.search(r'(\d+)\s*(?:week|wk|weeks|wks)', text_lower)
        if week_match:
            weeks = int(week_match.group(1))
            duration_days = weeks * 7
        
        # Look for month patterns
        month_match = re.search(r'(\d+)\s*(?:month|months|mo)', text_lower)
        if month_match:
            months = int(month_match.group(1))
            duration_days = months * 30
        
        # Look for day patterns
        day_match = re.search(r'(\d+)\s*(?:day|days)', text_lower)
        if day_match:
            days = int(day_match.group(1))
            duration_days = max(duration_days, days)
        
        # Check for chronic markers
        if any(marker in text_lower for marker in self.temporal_markers["chronic"]):
            duration_days = max(duration_days, 90)  # Assume at least 3 months
        
        # Check for recent markers (assume ~2-4 weeks)
        if duration_days == 0 and any(marker in text_lower for marker in self.temporal_markers["recent"]):
            duration_days = 21  # Assume 3 weeks
        
        return duration_days
