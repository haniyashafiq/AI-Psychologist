"""
DSM-5-TR PDF Ingestion Script
Parses a DSM-5-TR PDF, chunks it semantically, generates embeddings,
and stores them in ChromaDB for RAG retrieval.

Usage:
    python scripts/ingest_pdf.py --pdf /path/to/DSM-5-TR.pdf
    python scripts/ingest_pdf.py --pdf /path/to/DSM-5-TR.pdf --dry-run
    python scripts/ingest_pdf.py --pdf /path/to/DSM-5-TR.pdf --collection dsm5 --chunk-size 800
"""
import argparse
import hashlib
import os
import re
import sys
import time
from typing import List, Dict, Any, Optional

# Add the parent directory to the path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extract text from PDF page by page with metadata.
    Returns a list of {page_num, text, headings} dicts.
    """
    print(f"Opening PDF: {pdf_path}")
    doc = fitz.open(pdf_path)
    pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")

        if text.strip():
            pages.append({
                "page_num": page_num + 1,  # 1-indexed
                "text": text.strip(),
            })

    doc.close()
    print(f"Extracted text from {len(pages)} pages (out of {page_num + 1} total)")
    return pages


# DSM-5-TR disorder section patterns for structured metadata
DSM_DISORDER_PATTERNS = {
    "Major Depressive Disorder": {
        "codes": ["F32", "F33", "F32.0", "F32.1", "F32.2", "F32.9", "F33.0", "F33.1", "F33.2", "F33.9"],
        "keywords": ["major depressive disorder", "major depressive episode", "MDD"],
    },
    "Persistent Depressive Disorder": {
        "codes": ["F34.1"],
        "keywords": ["persistent depressive", "dysthymia", "dysthymic"],
    },
    "Bipolar I Disorder": {
        "codes": ["F31"],
        "keywords": ["bipolar i disorder", "manic episode", "bipolar i"],
    },
    "Bipolar II Disorder": {
        "codes": ["F31.81"],
        "keywords": ["bipolar ii disorder", "hypomanic episode", "bipolar ii"],
    },
    "Generalized Anxiety Disorder": {
        "codes": ["F41.1"],
        "keywords": ["generalized anxiety disorder", "GAD"],
    },
    "Panic Disorder": {
        "codes": ["F41.0"],
        "keywords": ["panic disorder", "panic attack"],
    },
    "Social Anxiety Disorder": {
        "codes": ["F40.10"],
        "keywords": ["social anxiety disorder", "social phobia"],
    },
    "PTSD": {
        "codes": ["F43.10"],
        "keywords": ["posttraumatic stress disorder", "PTSD", "post-traumatic"],
    },
    "OCD": {
        "codes": ["F42"],
        "keywords": ["obsessive-compulsive disorder", "OCD"],
    },
    "Schizophrenia": {
        "codes": ["F20"],
        "keywords": ["schizophrenia", "schizophrenic"],
    },
    "ADHD": {
        "codes": ["F90"],
        "keywords": ["attention-deficit/hyperactivity", "ADHD", "attention deficit"],
    },
    "Autism Spectrum Disorder": {
        "codes": ["F84.0"],
        "keywords": ["autism spectrum disorder", "ASD", "autism"],
    },
    "Anorexia Nervosa": {
        "codes": ["F50.0"],
        "keywords": ["anorexia nervosa"],
    },
    "Bulimia Nervosa": {
        "codes": ["F50.2"],
        "keywords": ["bulimia nervosa"],
    },
    "Substance Use Disorders": {
        "codes": ["F10", "F11", "F12", "F13", "F14", "F15", "F16", "F19"],
        "keywords": ["substance use disorder", "substance-related", "alcohol use disorder"],
    },
    "Insomnia Disorder": {
        "codes": ["F51.01"],
        "keywords": ["insomnia disorder"],
    },
    "Adjustment Disorders": {
        "codes": ["F43.2"],
        "keywords": ["adjustment disorder"],
    },
}

# Section type detection patterns
SECTION_TYPE_PATTERNS = {
    "diagnostic_criteria": [
        r"diagnostic criteria",
        r"criterion [a-z]",
        r"criteria [a-z]",
        r"a\.\s+(five|four|three|two|one)\s+",
    ],
    "diagnostic_features": [
        r"diagnostic features",
        r"the essential feature",
        r"clinical features",
    ],
    "associated_features": [
        r"associated features",
        r"supporting diagnosis",
    ],
    "prevalence": [
        r"prevalence",
        r"epidemiolog",
    ],
    "development_and_course": [
        r"development and course",
        r"age at onset",
        r"course of",
    ],
    "risk_factors": [
        r"risk and prognostic factors",
        r"risk factors",
        r"temperamental",
        r"environmental\.",
        r"genetic and physiological",
    ],
    "differential_diagnosis": [
        r"differential diagnosis",
        r"distinguish.*from",
        r"differentiat",
    ],
    "comorbidity": [
        r"comorbidity",
        r"comorbid",
        r"co-occurring",
    ],
    "specifiers": [
        r"specifiers?",
        r"with anxious distress",
        r"with mixed features",
        r"with melancholic features",
        r"with atypical features",
        r"with psychotic features",
        r"with peripartum onset",
        r"with seasonal pattern",
    ],
    "severity": [
        r"severity",
        r"mild[,.]",
        r"moderate[,.]",
        r"severe[,.]",
        r"in partial remission",
        r"in full remission",
    ],
    "functional_consequences": [
        r"functional consequences",
        r"functional impairment",
        r"disability",
    ],
}


def detect_disorder(text: str) -> Optional[Dict[str, Any]]:
    """Detect which DSM-5 disorder a text chunk is about"""
    text_lower = text.lower()
    best_match = None
    best_score = 0

    for disorder_name, info in DSM_DISORDER_PATTERNS.items():
        score = 0
        matched_code = ""

        # Check for ICD codes
        for code in info["codes"]:
            if code.lower() in text_lower:
                score += 3
                matched_code = code
                break

        # Check for keywords
        for keyword in info["keywords"]:
            if keyword.lower() in text_lower:
                score += 2

        if score > best_score:
            best_score = score
            best_match = {
                "disorder_name": disorder_name,
                "disorder_code": matched_code or info["codes"][0],
                "match_score": score,
            }

    return best_match if best_score >= 2 else None


def detect_section_type(text: str) -> str:
    """Detect what type of DSM section this text belongs to"""
    text_lower = text.lower()

    for section_type, patterns in SECTION_TYPE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return section_type

    return "general"


def chunk_text(
    pages: List[Dict[str, Any]],
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> List[Dict[str, Any]]:
    """
    Chunk the extracted pages into semantically meaningful segments.
    Uses a combination of:
    1. Page boundaries
    2. Heading detection (uppercase lines, bold markers)
    3. Paragraph boundaries
    4. Size limits with overlap
    """
    chunks = []

    # First, merge all pages into sections based on heading detection
    sections = []
    current_section = {"title": "", "text": "", "start_page": 1, "end_page": 1}

    for page_data in pages:
        page_num = page_data["page_num"]
        text = page_data["text"]

        # Split into lines and look for section headings
        lines = text.split("\n")
        for line in lines:
            stripped = line.strip()
            if not stripped:
                current_section["text"] += "\n"
                continue

            # Detect heading-like lines (all caps, short, or contains disorder name patterns)
            is_heading = (
                (stripped.isupper() and len(stripped) > 3 and len(stripped) < 100)
                or re.match(r"^(Criterion|Criteria)\s+[A-Z]", stripped)
                or re.match(r"^(Diagnostic (Criteria|Features)|Differential Diagnosis|Associated Features|Prevalence|Development and Course|Risk and Prognostic Factors|Comorbidity|Specifiers|Functional Consequences)", stripped, re.IGNORECASE)
            )

            if is_heading and len(current_section["text"].strip()) > 50:
                # Save current section
                current_section["end_page"] = page_num
                sections.append(current_section)
                current_section = {
                    "title": stripped,
                    "text": stripped + "\n",
                    "start_page": page_num,
                    "end_page": page_num,
                }
            else:
                current_section["text"] += stripped + "\n"
                current_section["end_page"] = page_num

    # Don't forget the last section
    if current_section["text"].strip():
        sections.append(current_section)

    print(f"Identified {len(sections)} sections from page content")

    # Now chunk each section to the target size
    for section in sections:
        text = section["text"].strip()
        if not text:
            continue

        # If section fits in one chunk, keep it whole
        if len(text) <= chunk_size * 1.5:
            chunks.append({
                "text": text,
                "section_title": section["title"],
                "page_range": f"{section['start_page']}-{section['end_page']}",
            })
            continue

        # Split into paragraphs
        paragraphs = re.split(r"\n\s*\n", text)
        current_chunk = ""
        chunk_start_page = section["start_page"]

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            # If adding this paragraph would exceed chunk_size
            if len(current_chunk) + len(para) > chunk_size and current_chunk:
                chunks.append({
                    "text": current_chunk.strip(),
                    "section_title": section["title"],
                    "page_range": f"{chunk_start_page}-{section['end_page']}",
                })

                # Start new chunk with overlap from the end of the previous chunk
                overlap_text = current_chunk[-chunk_overlap:] if len(current_chunk) > chunk_overlap else current_chunk
                current_chunk = overlap_text + "\n\n" + para
            else:
                current_chunk += "\n\n" + para if current_chunk else para

        # Save remaining text
        if current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                "section_title": section["title"],
                "page_range": f"{chunk_start_page}-{section['end_page']}",
            })

    print(f"Created {len(chunks)} chunks")
    return chunks


def enrich_chunks_with_metadata(chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Add disorder detection and section type metadata to each chunk"""
    for idx, chunk in enumerate(chunks):
        text = chunk["text"]

        # Detect disorder
        disorder_info = detect_disorder(text)
        if disorder_info:
            chunk["disorder_name"] = disorder_info["disorder_name"]
            chunk["disorder_code"] = disorder_info["disorder_code"]
        else:
            chunk["disorder_name"] = "General"
            chunk["disorder_code"] = ""

        # Detect section type
        chunk["section_type"] = detect_section_type(text)

        # Generate a unique ID using content hash + index to avoid duplicates
        content_hash = hashlib.md5(text.encode()).hexdigest()[:10]
        chunk["id"] = f"dsm5_{idx:04d}_{content_hash}"

    return chunks


def ingest_to_chromadb(
    chunks: List[Dict[str, Any]],
    collection_name: str = "dsm5",
    chroma_persist_dir: str = "/data/chroma_db",
    batch_size: int = 50,
):
    """
    Generate embeddings and store chunks in ChromaDB.
    Uses the EmbeddingService for OpenAI embeddings.
    """
    from app.services.embedding_service import EmbeddingService
    from app.services.retrieval_service import RetrievalService
    from app.config.settings import settings

    # Override settings if provided
    settings.chroma_persist_dir = chroma_persist_dir
    settings.chroma_collection_name = collection_name

    embedding_service = EmbeddingService()
    retrieval_service = RetrievalService()

    # Delete existing collection for clean re-ingestion
    retrieval_service.delete_collection()
    # Re-initialize the collection
    retrieval_service._collection = None

    total = len(chunks)
    print(f"\nIngesting {total} chunks into ChromaDB collection '{collection_name}'")
    print(f"Persist directory: {chroma_persist_dir}")
    print(f"Embedding model: {settings.embedding_model}")
    print()

    for i in range(0, total, batch_size):
        batch = chunks[i : i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total + batch_size - 1) // batch_size

        print(f"  Batch {batch_num}/{total_batches}: Embedding {len(batch)} chunks...")

        texts = [c["text"] for c in batch]
        ids = [c["id"] for c in batch]
        metadatas = [
            {
                "section_title": c.get("section_title", ""),
                "disorder_name": c.get("disorder_name", "General"),
                "disorder_code": c.get("disorder_code", ""),
                "section_type": c.get("section_type", "general"),
                "page_range": c.get("page_range", ""),
            }
            for c in batch
        ]

        # Generate embeddings synchronously
        embeddings = embedding_service.embed_batch_sync(texts)

        # Store in ChromaDB
        retrieval_service.add_documents(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        print(f"    ✓ Batch {batch_num} stored successfully")

    final_count = retrieval_service.collection.count()
    print(f"\n✓ Ingestion complete! {final_count} documents in collection '{collection_name}'")
    return final_count


def main():
    parser = argparse.ArgumentParser(
        description="Ingest DSM-5-TR PDF into ChromaDB for RAG retrieval"
    )
    parser.add_argument(
        "--pdf",
        required=True,
        help="Path to the DSM-5-TR PDF file",
    )
    parser.add_argument(
        "--collection",
        default="dsm5",
        help="ChromaDB collection name (default: dsm5)",
    )
    parser.add_argument(
        "--chroma-dir",
        default=None,
        help="ChromaDB persist directory (default: from settings)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=800,
        help="Target chunk size in characters (default: 800)",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=150,
        help="Overlap between chunks in characters (default: 150)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and chunk the PDF without generating embeddings or storing",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Batch size for embedding generation (default: 50)",
    )

    args = parser.parse_args()

    # Validate PDF exists
    if not os.path.exists(args.pdf):
        print(f"Error: PDF not found at '{args.pdf}'")
        sys.exit(1)

    start_time = time.time()

    # Step 1: Extract text from PDF
    print("=" * 60)
    print("STEP 1: Extracting text from PDF")
    print("=" * 60)
    pages = extract_text_from_pdf(args.pdf)

    # Step 2: Chunk the text
    print("\n" + "=" * 60)
    print("STEP 2: Chunking text into segments")
    print("=" * 60)
    chunks = chunk_text(pages, args.chunk_size, args.chunk_overlap)

    # Step 3: Enrich with metadata
    print("\n" + "=" * 60)
    print("STEP 3: Enriching chunks with metadata")
    print("=" * 60)
    chunks = enrich_chunks_with_metadata(chunks)

    # Print stats
    disorder_counts = {}
    section_counts = {}
    for chunk in chunks:
        d = chunk.get("disorder_name", "Unknown")
        s = chunk.get("section_type", "unknown")
        disorder_counts[d] = disorder_counts.get(d, 0) + 1
        section_counts[s] = section_counts.get(s, 0) + 1

    print(f"\nChunk statistics:")
    print(f"  Total chunks: {len(chunks)}")
    print(f"  Avg chunk size: {sum(len(c['text']) for c in chunks) / len(chunks):.0f} chars")
    print(f"\n  By disorder:")
    for disorder, count in sorted(disorder_counts.items(), key=lambda x: -x[1]):
        print(f"    {disorder}: {count}")
    print(f"\n  By section type:")
    for section, count in sorted(section_counts.items(), key=lambda x: -x[1]):
        print(f"    {section}: {count}")

    if args.dry_run:
        print("\n" + "=" * 60)
        print("DRY RUN — Skipping embedding and storage")
        print("=" * 60)

        # Show sample chunks
        print("\nSample chunks:")
        for i, chunk in enumerate(chunks[:5]):
            print(f"\n--- Chunk {i+1} ---")
            print(f"  ID: {chunk['id']}")
            print(f"  Section: {chunk.get('section_title', 'N/A')}")
            print(f"  Disorder: {chunk.get('disorder_name', 'N/A')} ({chunk.get('disorder_code', 'N/A')})")
            print(f"  Type: {chunk.get('section_type', 'N/A')}")
            print(f"  Pages: {chunk.get('page_range', 'N/A')}")
            print(f"  Length: {len(chunk['text'])} chars")
            print(f"  Preview: {chunk['text'][:150]}...")

        elapsed = time.time() - start_time
        print(f"\nDry run completed in {elapsed:.1f}s")
        return

    # Step 4: Ingest into ChromaDB
    print("\n" + "=" * 60)
    print("STEP 4: Generating embeddings and storing in ChromaDB")
    print("=" * 60)

    from app.config.settings import settings

    chroma_dir = args.chroma_dir or settings.chroma_persist_dir
    doc_count = ingest_to_chromadb(
        chunks=chunks,
        collection_name=args.collection,
        chroma_persist_dir=chroma_dir,
        batch_size=args.batch_size,
    )

    elapsed = time.time() - start_time
    print(f"\n{'=' * 60}")
    print(f"INGESTION COMPLETE")
    print(f"{'=' * 60}")
    print(f"  Documents stored: {doc_count}")
    print(f"  Collection: {args.collection}")
    print(f"  ChromaDB dir: {chroma_dir}")
    print(f"  Total time: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
