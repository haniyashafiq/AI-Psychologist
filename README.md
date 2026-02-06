# AI Psychologist - Depression Diagnosis Assistant

A web-based diagnostic assistant for Major Depressive Disorder (MDD) using natural language processing and DSM-5 criteria. Built for use by qualified mental health professionals.

## 🎯 Overview

This system uses a **rule-based approach** to analyze patient symptom descriptions in natural language and provide diagnostic assessments based on DSM-5 criteria for Major Depressive Disorder. The MVP focuses exclusively on MDD diagnosis with plans to expand to other depression types.

### Key Features

- ✅ **Natural Language Input**: Free-form text symptom descriptions
- ✅ **DSM-5 Compliant**: Implements all 9 MDD criteria (A1-A9)
- ✅ **Severity Assessment**: Calculates mild/moderate/severe with functional impairment
- ✅ **Crisis Detection**: Automatic flagging of suicidal ideation (A9)
- ✅ **Rule-Based NLP**: No external AI services (OpenAI, Claude, etc.)
- ✅ **Custom Symptom Vocabulary**: ~100 colloquial terms mapped to clinical symptoms
- ✅ **Negation Detection**: Handles phrases like "I do NOT feel sad"
- ✅ **Functional Impairment Analysis**: Detects impact on daily activities

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────────┐
│  React/Vite     │  HTTP   │  Express.js      │  HTTP   │  Python FastAPI     │
│  Frontend       │────────▶│  Backend         │────────▶│  NLP Service        │
│  (Port 5173)    │         │  (Port 3000)     │         │  (Port 8000)        │
└─────────────────┘         └──────────────────┘         └─────────────────────┘
                                     │                             │
                                     │                             │
                                     ▼                             ▼
                            ┌─────────────────┐         ┌────────────────────┐
                            │ Diagnosis Engine│         │ spaCy NLP Engine   │
                            │ (DSM-5 Rules)   │         │ Symptom Extraction │
                            └─────────────────┘         └────────────────────┘
```

### Technology Stack

| Layer           | Technology                        | Purpose                              |
| --------------- | --------------------------------- | ------------------------------------ |
| **Frontend**    | React 18 + Vite                   | User interface                       |
| **Styling**     | Tailwind CSS                      | Responsive design                    |
| **Backend API** | Express.js 4                      | REST API server                      |
| **NLP Service** | Python FastAPI                    | Symptom extraction                   |
| **NLP Engine**  | spaCy 3.7                         | Pattern matching, negation detection |
| **Validation**  | Joi (Backend), Zod (Frontend)     | Input validation                     |
| **Logging**     | Winston (Backend), Python logging | Application logs                     |

## 📁 Project Structure

```
AI-Psychologist/
├── frontend/               # React + Vite UI
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API client
│   │   └── hooks/         # Custom React hooks
│   └── package.json
│
├── backend/               # Express.js API
│   ├── src/
│   │   ├── services/      # Business logic (diagnosis, severity, NLP client)
│   │   ├── routes/        # API routes
│   │   ├── controllers/   # Request handlers
│   │   ├── models/        # MDD criteria definitions
│   │   └── middleware/    # Validation, error handling, CORS
│   └── package.json
│
├── nlp-service/           # Python NLP service
│   ├── app/
│   │   ├── services/      # Symptom extraction, negation detection
│   │   ├── models/        # Symptom patterns and vocabulary
│   │   ├── api/           # FastAPI routes and schemas
│   │   └── config/        # Settings
│   └── requirements.txt
│
└── shared/                # Shared documentation
    ├── docs/              # Project documentation
    └── data/              # Test cases and examples
```

## 🚀 Quick Start

### Prerequisites

- **Node.js 18+** and npm
- **Python 3.10+** and pip
- **Git**

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd AI-Psychologist
```

2. **Set up Python NLP Service**

```bash
cd nlp-service
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_md
```

3. **Set up Backend**

```bash
cd ../backend
npm install
```

4. **Set up Frontend**

```bash
cd ../frontend
npm install
```

### Running the Application

You'll need **3 terminal windows**:

**Terminal 1 - NLP Service:**

```bash
cd nlp-service
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m app.main
# Runs on http://localhost:8000
```

**Terminal 2 - Backend:**

```bash
cd backend
npm run dev
# Runs on http://localhost:3000
```

**Terminal 3 - Frontend:**

```bash
cd frontend
npm run dev
# Runs on http://localhost:5173
```

Open your browser to **http://localhost:5173**

## 🧪 Testing

### Sample Input

Try this example text in the assessment form:

```
I've been feeling really down for the past few weeks. I can't seem to enjoy anything
anymore, not even activities I used to love. I'm having trouble sleeping at night -
I lie awake for hours. During the day, I feel completely exhausted and have no energy
to do anything. I've lost my appetite and dropped about 10 pounds. I feel worthless
and guilty about everything, even things that aren't my fault. It's hard to concentrate
at work, and I can't make simple decisions. I just feel like there's no point to anything.
```

**Expected Result:**

- **Diagnosis**: Major Depressive Disorder criteria met (7-8 symptoms)
- **Severity**: Moderate
- **Symptoms Detected**: A1 (depressed mood), A2 (anhedonia), A3 (weight/appetite), A4 (insomnia), A6 (fatigue), A7 (worthlessness), A8 (concentration)

## 📊 DSM-5 MDD Diagnostic Criteria

The system implements the complete DSM-5 criteria for Major Depressive Disorder:

| Code   | Symptom           | Description                                   |
| ------ | ----------------- | --------------------------------------------- |
| **A1** | Depressed Mood    | Sad, empty, or hopeless mood most of the day  |
| **A2** | Anhedonia         | Loss of interest or pleasure in activities    |
| **A3** | Weight/Appetite   | Significant weight change or appetite change  |
| **A4** | Sleep             | Insomnia or hypersomnia nearly every day      |
| **A5** | Psychomotor       | Agitation or retardation observable by others |
| **A6** | Fatigue           | Fatigue or loss of energy nearly every day    |
| **A7** | Worthlessness     | Feelings of worthlessness or excessive guilt  |
| **A8** | Concentration     | Diminished ability to think or concentrate    |
| **A9** | Suicidal Ideation | Thoughts of death or suicide                  |

**Diagnostic Thresholds:**

- **Required**: 5+ symptoms (including A1 or A2)
- **Duration**: 2+ weeks
- **Severity**: Mild (5-6), Moderate (7-8), Severe (9)

## 🔍 How It Works

### 1. Symptom Extraction (NLP Service)

```
Input Text → spaCy Processing → Pattern Matching → Negation Detection → Symptom List
```

- **Pattern Matching**: Token-based patterns + phrase matching + keyword fallback
- **Negation Detection**: Identifies "NOT sad" vs "sad"
- **Temporal Extraction**: Detects duration ("for 3 weeks")
- **Functional Impairment**: Keywords like "can't work", "stopped socializing"

### 2. Diagnosis (Backend)

```
Symptoms → Map to DSM-5 → Apply Rules → Calculate Severity → Generate Recommendations
```

- **Rule Engine**: Checks symptom count, core symptoms (A1/A2), duration
- **Severity Calculator**: Uses symptom count + functional impairment
- **Crisis Detection**: Flags A9 (suicidal ideation) for immediate intervention

### 3. Display (Frontend)

- Visual severity indicator (color-coded)
- Detailed symptom breakdown with evidence
- Actionable recommendations
- Crisis alerts with hotline numbers
- Professional disclaimer

## 📝 API Documentation

### Backend API

**Base URL**: `http://localhost:3000/api/v1`

#### Analyze Symptoms

```http
POST /assessment/analyze
Content-Type: application/json

{
  "text": "Patient symptom description..."
}
```

**Response**:

```json
{
  "success": true,
  "data": {
    "diagnosis": {
      "condition": "Major Depressive Disorder",
      "meetsThreshold": true,
      "confidence": "high",
      "criteriaMetCount": 7,
      "crisisDetected": false
    },
    "severity": {
      "level": "moderate",
      "score": 7,
      "functionalImpairment": true
    },
    "symptoms": [...],
    "recommendations": [...]
  }
}
```

### NLP Service API

**Base URL**: `http://localhost:8000`

#### Extract Symptoms

```http
POST /nlp/extract-symptoms
Content-Type: application/json

{
  "text": "I feel sad and empty..."
}
```

## 🛡️ Important Disclaimers

⚠️ **THIS IS NOT A SUBSTITUTE FOR PROFESSIONAL DIAGNOSIS**

- This tool is designed for use by **qualified mental health professionals only**
- It is a **screening tool**, not a diagnostic instrument
- Only licensed psychiatrists/psychologists can provide official diagnoses
- All assessments should be part of comprehensive clinical evaluation

## 🗺️ Future Enhancements

### Phase 2: Expand Depression Types

- [ ] Persistent Depressive Disorder (Dysthymia)
- [ ] Premenstrual Dysphoric Disorder
- [ ] Disruptive Mood Dysregulation Disorder

### Phase 3: Advanced Features

- [ ] Multi-language support
- [ ] Historical tracking and progress monitoring
- [ ] Enhanced functional impairment scoring
- [ ] Export reports to PDF
- [ ] Integration with EHR systems

### Phase 4: ML Enhancements (Optional)

- [ ] Fine-tune transformer model for better symptom extraction
- [ ] Hybrid approach: LLM preprocessing + rule-based diagnosis

## 📄 License

[Specify your license]

## 👥 Contributors

[Your name/team]

## 🙏 Acknowledgments

- DSM-5 Diagnostic Criteria from American Psychiatric Association
- spaCy NLP library
- Open-source community

---

**Version**: 1.0.0 (MVP - Major Depressive Disorder Only)  
**Last Updated**: February 2026
