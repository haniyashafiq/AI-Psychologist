"""Query template builders for RAG-augmented prompts"""
from typing import List, Dict, Any, Optional


def build_assessment_prompt(
    patient_text: str,
    retrieved_context: List[Dict[str, Any]],
    detected_symptoms: Optional[List[Dict[str, Any]]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Build the user prompt for clinical assessment, combining:
    - Retrieved DSM-5-TR context from vector search
    - Patient presentation text
    - NLP-detected symptoms (if available)
    """

    sections = []

    # Section 1: Retrieved DSM-5-TR Context
    sections.append("=" * 60)
    sections.append("RETRIEVED DSM-5-TR REFERENCE MATERIAL")
    sections.append("=" * 60)

    if retrieved_context:
        for i, ctx in enumerate(retrieved_context, 1):
            doc_text = ctx.get("document", "")
            meta = ctx.get("metadata", {})
            distance = ctx.get("distance", None)

            sections.append(f"\n--- Reference {i} ---")
            if meta.get("section_title"):
                sections.append(f"Section: {meta['section_title']}")
            if meta.get("disorder_name"):
                sections.append(f"Disorder: {meta['disorder_name']}")
            if meta.get("disorder_code"):
                sections.append(f"Code: {meta['disorder_code']}")
            if meta.get("page_range"):
                sections.append(f"Pages: {meta['page_range']}")
            if meta.get("section_type"):
                sections.append(f"Type: {meta['section_type']}")
            if distance is not None:
                relevance = max(0, 1 - distance)  # cosine distance to similarity
                sections.append(f"Relevance Score: {relevance:.2f}")
            sections.append(f"\n{doc_text}")
    else:
        sections.append("No relevant DSM-5-TR references were retrieved.")
        sections.append("Provide assessment based on general DSM-5-TR knowledge.")

    # Section 2: NLP-Detected Symptoms
    if detected_symptoms:
        sections.append("\n" + "=" * 60)
        sections.append("PRE-SCREENING: NLP-DETECTED SYMPTOMS")
        sections.append("=" * 60)
        sections.append(
            "The following symptoms were detected by automated NLP pattern matching. "
            "Use these as a starting point but apply your own clinical judgment."
        )

        for symptom in detected_symptoms:
            if symptom.get("detected"):
                status = "DETECTED"
                confidence = symptom.get("confidence", 0)
                evidence = symptom.get("evidence", [])
                context = symptom.get("sentenceContext", "")

                sections.append(
                    f"\n• [{status}] {symptom.get('dsm5Code', '?')}: "
                    f"{symptom.get('name', 'Unknown')}"
                )
                sections.append(f"  Confidence: {confidence:.0%}")
                if evidence:
                    sections.append(f"  Evidence: {', '.join(evidence)}")
                if context:
                    sections.append(f"  Context: \"{context}\"")

        not_detected = [s for s in detected_symptoms if not s.get("detected")]
        if not_detected:
            sections.append("\nNot detected by NLP:")
            for symptom in not_detected:
                sections.append(
                    f"  ○ {symptom.get('dsm5Code', '?')}: "
                    f"{symptom.get('name', 'Unknown')}"
                )

    # Section 3: Metadata
    if metadata:
        sections.append("\n" + "=" * 60)
        sections.append("ADDITIONAL CONTEXT")
        sections.append("=" * 60)
        if metadata.get("durationDays"):
            sections.append(f"Reported duration: {metadata['durationDays']} days")
        if metadata.get("durationSpecified") is False:
            sections.append("Duration was NOT specified in the text")
        if metadata.get("functionalImpairment"):
            sections.append(
                f"Functional impairment detected: {metadata['functionalImpairment']}"
            )

    # Section 4: Patient Presentation
    sections.append("\n" + "=" * 60)
    sections.append("PATIENT PRESENTATION (ORIGINAL TEXT)")
    sections.append("=" * 60)
    sections.append(patient_text)

    # Section 5: Assessment Task
    sections.append("\n" + "=" * 60)
    sections.append("ASSESSMENT TASK")
    sections.append("=" * 60)
    sections.append(
        "Based on the DSM-5-TR reference material above and the patient presentation, "
        "provide a comprehensive clinical decision-support assessment. "
        "Cite specific DSM-5-TR criteria from the retrieved references. "
        "Consider differential diagnoses beyond MDD. "
        "Identify any gaps in the clinical picture that would need further evaluation. "
        "Respond in the JSON format specified in your system instructions."
    )

    return "\n".join(sections)


def build_retrieval_query(
    patient_text: str,
    detected_symptoms: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """
    Build an optimized query for vector retrieval.
    Combines patient text with detected symptom names for better semantic matching.
    """
    parts = [patient_text]

    if detected_symptoms:
        symptom_names = [
            s.get("name", "")
            for s in detected_symptoms
            if s.get("detected") and s.get("name")
        ]
        if symptom_names:
            parts.append(
                "DSM-5 diagnostic criteria for: " + ", ".join(symptom_names)
            )

    return " ".join(parts)
