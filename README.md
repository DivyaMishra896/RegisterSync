# Suraksha — Regulatory Compliance Automation

**AI-powered compliance automation platform for Indian banking.** Upload RBI/SEBI circulars, extract rules with AI, generate measurable action points, route tasks to departments, and auto-verify compliance — all from a single dashboard.

---

## Key Features

| Module | Description |
|--------|-------------|
| **PDF Ingestion** | Upload RBI/SEBI circular PDFs with drag-and-drop. Automatic text extraction and chunking. |
| **AI Rule Extraction** | Claude API (or mock) extracts structured rules with priorities, deadlines, and department assignments. |
| **MAP Generator** | Converts rules into Measurable Action Points (MAPs) with auto-routing to IT Security, Risk Management, or Operations. |
| **Conflict Checker** | Detects contradictions between new and existing regulations (e.g., "2026 circular contradicts 2021 data localization policy"). |
| **Verification Agent** | Reads system logs to auto-verify task completion. Flips status from Pending to Verified/Failed/Partially Done with audit trail. |
| **Impact Predictor** | Visual charts showing estimated effort by department and compliance status breakdown. |

---

## Quick Start

### Prerequisites
- Python 3.11+ 
- Node.js 18+
- npm

### Backend Setup
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

# Generate mock RBI circular PDF
python generate_mock_pdf.py

# Start the API server
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Access the App
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/api/health

---

## Demo Flow (3-minute walkthrough)

1. **Upload** (30s) — Drag the included `mock_rbi_circular.pdf` from `/backend/samples/` onto the upload screen
2. **AI Extract** (45s) — Click "Extract Rules with AI" to see the LLM analyzing the circular and producing structured MAPs in real time
3. **Dashboard** (45s) — Navigate to the Compliance Dashboard to see tasks assigned to IT Security, Risk Management, and Operations with deadlines and priorities
4. **Conflict Check** (30s) — Observe the AI flagging that the new VAPT rule supersedes the 2022 quarterly schedule, and that data localization contradicts the 2021 overseas storage policy
5. **Verification** (30s) — Click "Run Verification" and watch tasks flip from Pending to Verified as the agent reads mock system logs. Hold on this moment - it's the most visually compelling beat.

---

## Architecture

```
PDF Upload -> Text Extraction (PyMuPDF) -> AI Analysis (Claude API)
    -> Rule Extraction -> Conflict Detection -> MAP Generation
    -> Department Routing -> Task Dashboard -> Verification Agent
```

### Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, Vite, Recharts, Lucide Icons |
| **Backend** | Python 3.11, FastAPI, Uvicorn |
| **AI / LLM** | Claude Sonnet API (with mock mode) |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **PDF Parsing** | PyMuPDF |

---

## Project Structure

```
Suraksha/
├── backend/
│   ├── main.py                  # FastAPI entry point
│   ├── config.py                # Settings & env loader
│   ├── database.py              # SQLAlchemy setup
│   ├── models/                  # ORM models (Circular, Rule, Task)
│   ├── routers/                 # API endpoints
│   ├── services/                # Business logic
│   │   ├── pdf_parser.py        # PDF text extraction
│   │   ├── llm_extractor.py     # Claude API / mock extractor
│   │   ├── map_generator.py     # Rule -> Task conversion
│   │   ├── department_router.py # Keyword-based dept routing
│   │   ├── conflict_checker.py  # Old vs new rule conflicts
│   │   └── verification_agent.py # Log-based auto-verification
│   ├── mock_logs/               # Mock compliance logs
│   └── samples/                 # Sample circulars
│
├── frontend/
│   └── src/
│       ├── api/client.js        # Axios API client
│       ├── components/          # React components
│       └── pages/               # Page components
│
└── README.md
```

---

## Configuration

Copy `.env.example` to `.env` in the `backend/` directory:

```env
# Use "mock" for demo (no API key needed)
# Use "live" for real Claude API
LLM_MODE=mock

# Only needed if LLM_MODE=live
ANTHROPIC_API_KEY=sk-ant-xxxxx

DATABASE_URL=sqlite:///./suraksha.db
FRONTEND_URL=http://localhost:5173
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/upload` | Upload a PDF circular |
| GET | `/api/upload/circulars` | List all circulars |
| POST | `/api/extract/{id}` | Trigger AI extraction |
| GET | `/api/tasks` | List tasks (filterable) |
| GET | `/api/tasks/stats` | Dashboard statistics |
| POST | `/api/verify/run` | Run verification agent |
| GET | `/api/verify/summary` | Compliance summary |

Full interactive API docs available at `/docs` (Swagger UI).

---

## What Makes Suraksha Different

**The Verification Agent** is the standout differentiator. While other compliance tools stop at task creation, Suraksha goes further:
- Reads actual system logs (mock in prototype, real SIEM/GRC integration in production)
- Auto-verifies whether compliance tasks have been implemented
- Creates an audit trail with timestamps and evidence links
- Flags partially completed or failed implementations
- The Pending → Verified status flip is the single most compelling demo moment

---

## License

MIT License - Built for Hackathon Prototype
