"""Symptom extraction using spaCy and pattern matching"""
from typing import List, Dict, Any
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Doc
from app.models.symptom_patterns import SYMPTOM_PATTERNS
from app.services.negation_detector import NegationDetector
from app.services.text_processor import TextProcessor
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class SymptomExtractor:
    """Extracts depression symptoms from natural language text"""
    
    def __init__(self, nlp):
        """
        Initialize symptom extractor
        
        Args:
            nlp: spaCy language model
        """
        self.nlp = nlp
        self.negation_detector = NegationDetector()
        self.text_processor = TextProcessor()
        self.symptom_patterns = SYMPTOM_PATTERNS
        
        # Store mapping of hash to symptom_id
        self.match_id_to_symptom = {}
        
        # Initialize matchers
        self.matcher = Matcher(nlp.vocab)
        self.phrase_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
        
        self._load_patterns()
    
    def _load_patterns(self):
        """Load symptom patterns into matchers"""
        for symptom_code, symptom_data in self.symptom_patterns.items():
            symptom_id = symptom_data["id"]
            
            # Add token-based patterns
            if "token_patterns" in symptom_data:
                for pattern in symptom_data["token_patterns"]:
                    self.matcher.add(f"{symptom_id}_token", [pattern])
            
            # Add phrase patterns and store mapping
            if "phrases" in symptom_data:
                patterns = [self.nlp.make_doc(phrase) for phrase in symptom_data["phrases"]]
                self.phrase_matcher.add(symptom_id, patterns)
                # Store the hash to symptom_id mapping
                hash_value = self.nlp.vocab.strings[symptom_id]
                self.match_id_to_symptom[hash_value] = symptom_id
        
        logger.info(f"Loaded {len(self.matcher)} token patterns and phrase patterns for symptom extraction")
    
    def extract(self, text: str) -> Dict[str, Any]:
        """
        Extract symptoms from text
        
        Args:
            text: Natural language input describing symptoms
            
        Returns:
            Dict containing extracted symptoms and metadata
        """
        # Clean text
        cleaned_text = self.text_processor.clean_text(text)
        
        # Process with spaCy
        doc = self.nlp(cleaned_text)
        
        # Extract symptoms
        symptoms = []
        detected_symptom_ids = set()
        
        # Process token-based matches
        token_matches = self.matcher(doc)
        for match_id, start, end in token_matches:
            symptom = self._process_match(doc, start, end, "token", match_id=match_id)
            if symptom and symptom["symptom_id"] not in detected_symptom_ids:
                symptoms.append(symptom)
                detected_symptom_ids.add(symptom["symptom_id"])
        
        # Process phrase-based matches
        phrase_matches = self.phrase_matcher(doc)
        for match_id, start, end in phrase_matches:
            # Use our mapping instead of vocab.strings
            symptom_id = self.match_id_to_symptom.get(match_id)
            if not symptom_id:
                logger.warning(f"Unknown match_id: {match_id}")
                continue
            symptom = self._process_match(doc, start, end, "phrase", symptom_id)
            if symptom and symptom["symptom_id"] not in detected_symptom_ids:
                symptoms.append(symptom)
                detected_symptom_ids.add(symptom["symptom_id"])
        
        # Fallback: keyword matching for missed symptoms
        keyword_symptoms = self._keyword_fallback(cleaned_text, detected_symptom_ids)
        symptoms.extend(keyword_symptoms)
        
        # Extract temporal and intensity markers
        temporal_markers = self.text_processor.extract_temporal_markers(cleaned_text)
        intensity_markers = self.text_processor.extract_intensity_markers(cleaned_text)
        functional_impairment = self.text_processor.detect_functional_impairment(cleaned_text)
        duration_days = self.text_processor.extract_duration_days(cleaned_text)
        
        return {
            "symptoms": symptoms,
            "metadata": {
                "tokens_count": len(doc),
                "sentences_count": len(list(doc.sents)),
                "temporal_markers": temporal_markers,
                "intensity_markers": intensity_markers,
                "functional_impairment": functional_impairment,
                "duration_days": duration_days
            }
        }
    
    def _process_match(self, doc: Doc, start: int, end: int, match_type: str, symptom_id: str = None, match_id: int = None) -> Dict[str, Any]:
        """Process a matched phrase and create symptom object"""
        span = doc[start:end]
        matched_text = span.text
        
        # Determine symptom ID
        if symptom_id is None and match_id is not None:
            # Extract from matcher label (for token matches)
            label = doc.vocab.strings[match_id]
            # Remove "_token" suffix to get symptom_id
            symptom_id = label.replace("_token", "") if label.endswith("_token") else label
        
        # Find corresponding symptom data
        symptom_data = None
        dsm5_code = None
        for code, data in self.symptom_patterns.items():
            if data["id"] == symptom_id:
                symptom_data = data
                dsm5_code = code
                break
        
        if not symptom_data:
            return None
        
        # Check for negation
        is_negated = self.negation_detector.is_negated(doc, start, end)
        
        if is_negated:
            logger.debug(f"Skipping negated symptom: {matched_text}")
            return None
        
        # Get sentence context
        sentence = None
        for sent in doc.sents:
            if sent.start <= start < sent.end:
                sentence = sent.text
                break
        
        # Calculate confidence (simple heuristic)
        confidence = 0.8 if match_type == "phrase" else 0.7
        
        return {
            "symptom_id": symptom_id,
            "dsm5_code": dsm5_code,
            "name": symptom_data["name"],
            "detected": True,
            "confidence": confidence,
            "matched_phrases": [matched_text.lower()],
            "sentence_context": sentence,
            "is_negated": False,
            "match_type": match_type
        }
    
    def _keyword_fallback(self, text: str, already_detected: set) -> List[Dict[str, Any]]:
        """Fallback keyword matching for symptoms missed by pattern matching"""
        text_lower = text.lower()
        fallback_symptoms = []
        
        for code, symptom_data in self.symptom_patterns.items():
            symptom_id = symptom_data["id"]
            
            # Skip if already detected
            if symptom_id in already_detected:
                continue
            
            # Check keywords
            matched_keywords = []
            for keyword in symptom_data["keywords"]:
                if keyword in text_lower:
                    # Simple negation check
                    if not self.negation_detector.check_phrase_negation(text, keyword):
                        matched_keywords.append(keyword)
            
            # If keywords found, add symptom with lower confidence
            if matched_keywords:
                fallback_symptoms.append({
                    "symptom_id": symptom_id,
                    "dsm5_code": code,
                    "name": symptom_data["name"],
                    "detected": True,
                    "confidence": 0.6,  # Lower confidence for keyword matching
                    "matched_phrases": matched_keywords,
                    "sentence_context": None,
                    "is_negated": False,
                    "match_type": "keyword"
                })
                already_detected.add(symptom_id)
        
        return fallback_symptoms
    
    def get_symptom_summary(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of extracted symptoms"""
        symptoms = extracted_data["symptoms"]
        metadata = extracted_data["metadata"]
        
        # Count by DSM-5 code
        symptom_counts = {}
        for symptom in symptoms:
            code = symptom["dsm5_code"]
            if code not in symptom_counts:
                symptom_counts[code] = 0
            symptom_counts[code] += 1
        
        # Check for crisis flag (suicidal ideation)
        crisis_detected = any(
            symptom["symptom_id"] == "suicidal_ideation" 
            for symptom in symptoms
        )
        
        return {
            "total_symptoms_detected": len(symptoms),
            "unique_symptoms": len(set(s["symptom_id"] for s in symptoms)),
            "symptom_codes": list(symptom_counts.keys()),
            "crisis_flag": crisis_detected,
            "duration_specified": metadata["duration_days"] > 0,
            "duration_days": metadata["duration_days"],
            "functional_impairment_detected": metadata["functional_impairment"]["detected"]
        }
