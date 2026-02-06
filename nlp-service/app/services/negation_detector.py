"""Negation detection for symptom extraction"""
import re
from typing import List, Tuple
from app.models.symptom_patterns import NEGATION_TERMS
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class NegationDetector:
    """Detects negation in text to avoid false positive symptom detection"""
    
    def __init__(self):
        self.negation_terms = NEGATION_TERMS
        self.negation_window = 3  # words before/after to check
    
    def is_negated(self, doc, start_idx: int, end_idx: int) -> bool:
        """
        Check if a phrase is negated based on surrounding context
        
        Args:
            doc: spaCy Doc object
            start_idx: Start token index of phrase
            end_idx: End token index of phrase
            
        Returns:
            bool: True if phrase appears to be negated
        """
        # Check tokens before the phrase
        window_start = max(0, start_idx - self.negation_window)
        
        for i in range(window_start, start_idx):
            token = doc[i]
            if token.text.lower() in self.negation_terms:
                # Check if there's a "but" or "however" that reverses negation
                reverse_found = False
                for j in range(i + 1, min(end_idx + 3, len(doc))):
                    if doc[j].text.lower() in ["but", "however", "although", "though"]:
                        reverse_found = True
                        break
                
                if not reverse_found:
                    logger.debug(f"Negation detected: '{token.text}' before phrase")
                    return True
        
        # Check within the phrase itself
        for i in range(start_idx, end_idx):
            if doc[i].text.lower() in self.negation_terms:
                logger.debug(f"Negation detected within phrase: '{doc[i].text}'")
                return True
        
        return False
    
    def check_phrase_negation(self, text: str, phrase: str) -> bool:
        """
        Simple string-based negation check (fallback for non-spaCy processing)
        
        Args:
            text: Full text
            phrase: Phrase to check
            
        Returns:
            bool: True if phrase appears negated
        """
        text_lower = text.lower()
        phrase_lower = phrase.lower()
        
        # Find phrase position
        phrase_pos = text_lower.find(phrase_lower)
        if phrase_pos == -1:
            return False
        
        # Check preceding words
        preceding = text_lower[max(0, phrase_pos - 50):phrase_pos]
        for neg_term in self.negation_terms:
            if neg_term in preceding.split()[-5:]:  # Last 5 words
                return True
        
        return False
