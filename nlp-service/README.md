# NLP Service - Depression Diagnosis

Python FastAPI service for extracting depression symptoms from natural language text using rule-based NLP with spaCy.

## Setup

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Download spaCy model:

```bash
python -m spacy download en_core_web_md
```

### Running the Service

```bash
# Development mode
python -m app.main

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The service will be available at `http://localhost:8000`

## API Endpoints

### Health Check

```bash
GET /health
```

### Extract Symptoms

```bash
POST /nlp/extract-symptoms
Content-Type: application/json

{
  "text": "I feel sad and empty most of the time. I can't sleep at night and have no energy during the day. Nothing interests me anymore and I feel worthless."
}
```

Response:

```json
{
  "success": true,
  "data": {
    "symptoms": [...],
    "metadata": {
      "tokens_count": 120,
      "duration_days": 0,
      "functional_impairment": {...}
    },
    "summary": {
      "total_symptoms_detected": 5,
      "unique_symptoms": 5,
      "crisis_flag": false
    }
  }
}
```

## Features

- **9 DSM-5 MDD Symptoms**: Detects all Major Depressive Disorder criteria (A1-A9)
- **Negation Detection**: Handles phrases like "I do NOT feel sad"
- **Temporal Markers**: Extracts duration information (weeks, months)
- **Functional Impairment**: Detects impact on daily activities
- **Intensity Markers**: Identifies severity indicators (very, extremely, slightly)
- **Crisis Detection**: Flags suicidal ideation (A9)

## Testing

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

## Development

Format code:

```bash
black app/
```

Lint:

```bash
flake8 app/
```

Type checking:

```bash
mypy app/
```
