# Frontend - Depression Diagnosis UI

React + Vite frontend application for the AI Psychologist depression diagnosis system.

## Setup

### Prerequisites

- Node.js 18+
- npm

### Installation

1. Install dependencies:

```bash
npm install
```

2. Configure environment:

```bash
cp .env.development .env
# Edit .env if needed
```

3. Ensure backend API is running on `http://localhost:3000`

### Running the Application

```bash
# Development mode (with hot reload)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

The application will be available at `http://localhost:5173`

## Features

- **Free-Form Text Input**: Enter patient symptoms in natural language
- **Real-Time Analysis**: Get immediate diagnostic assessment
- **Comprehensive Reports**: View detailed symptom breakdown, severity, and recommendations
- **Crisis Detection**: Automatic flagging of suicidal ideation
- **Professional UI**: Clean, accessible interface designed for clinical use
- **Responsive Design**: Works on desktop and tablet devices

## Components

### Assessment Components

- **TextInputForm**: Main symptom input form with validation
- **DiagnosisReport**: Complete diagnostic report display
- **SeverityIndicator**: Visual severity level indicator
- **RecommendationsCard**: Actionable recommendations

### Common Components

- **Button**: Reusable button with loading states
- **Spinner**: Loading indicator

## API Integration

The frontend communicates with the Express backend API at:

- Analyze endpoint: `POST /api/v1/assessment/analyze`
- Health check: `GET /api/v1/health`

See `src/services/api.js` for API client implementation.

## Technology Stack

- **React 18**: UI library
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Styling
- **Axios**: HTTP client
- **React Hook Form**: Form handling
- **Zustand**: State management (lightweight)

## Building for Production

```bash
npm run build
```

Output will be in `dist/` directory. Serve with any static file server.

## Environment Variables

- `VITE_API_BASE_URL`: Backend API URL (default: http://localhost:3000)
- `VITE_API_TIMEOUT`: API request timeout in ms (default: 30000)
