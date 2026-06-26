<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/Vite-8-646CFF?style=for-the-badge&logo=vite&logoColor=white" />
  <img src="https://img.shields.io/badge/Ollama-Local_LLM-000000?style=for-the-badge&logo=ollama&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

# RegisterSync — AI-Powered Regulatory Compliance Automation

> **Automate the end-to-end compliance lifecycle for Indian banking.**  
> Upload RBI/SEBI circulars → AI extracts rules → generates action items → routes to departments → auto-verifies completion — all from a single dashboard.

---

## What It Does

RegisterSync transforms a **multi-page regulatory PDF** into **department-level compliance tasks** in seconds. A multi-agent AI pipeline reads the circular, extracts structured rules, detects conflicts with existing regulations, routes tasks to the right teams, and even verifies implementation by reading system logs.

### Core Capabilities

| Capability | Description |
|:--|:--|
| **PDF Ingestion** | Drag-and-drop upload of RBI/SEBI circular PDFs. Automatic text extraction via PyMuPDF with intelligent chunking. |
| **Multi-Agent AI Extraction** | An orchestrated pipeline of specialized agents (Reader → Extractor → Conflict → Router) powered by Ollama (deepseek-r1) with NLP fallback. Live-streamed agent thoughts via SSE. |
| **MAP Generation** | Converts extracted rules into **Measurable Action Points** with auto-assigned departments, priorities, deadlines, and effort estimates. |
| **Conflict Detection** | TF-IDF cosine similarity + semantic analysis to flag contradictions between new and existing regulations — e.g., _"2026 data localization rule contradicts 2021 overseas storage policy."_ |
| **Verification Agent** | Reads mock system logs (SIEM/GRC in production) to auto-verify task completion. Flips status from `Pending` → `Verified` / `Failed` / `Partially Done` with full audit trail. |
| **Risk & Impact Dashboard** | Real-time compliance rate, risk scoring, effort-by-department charts, and priority breakdowns powered by Recharts. |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FRONTEND  (React 19 + Vite 8)                │
│  UploadPage ──→ ExtractionView (SSE) ──→ DashboardPage              │
│  CircularsPage    TaskBoard / TaskCard    VerificationPanel         │
│                   ImpactPredictor         StatusBadge               │
└──────────────────────────┬──────────────────────────────────────────┘
                           │  REST + SSE
┌──────────────────────────▼──────────────────────────────────────────┐
│                        BACKEND  (FastAPI + Uvicorn)                 │
│                                                                     │
│  Routers:  upload │ extraction │ tasks │ verification               │
│                                                                     │
│  ┌─────────────── Multi-Agent Pipeline ──────────────┐              │
│  │  Orchestrator                                     │              │
│  │    ├── ReaderAgent     → Document structure       │             │
│  │    ├── ExtractorAgent  → Rule extraction          │             │
│  │    ├── ConflictAgent   → Cross-regulation check   │             │
│  │    └── RouterAgent     → Department assignment    │             │
│  └───────────────────────────────────────────────────┘              │
│                                                                     │
│  Services:  pdf_parser │ llm_provider │ llm_extractor │             │
│             map_generator │ department_router │ conflict_checker    │
│             verification_agent │ nlp_fallback │ department_data     │
│                                                                     │
│  Database:  SQLite (SQLAlchemy ORM)                                 │
│  Models:    Circular │ ExtractedRule │ MAPTask                      │
└──────────────────────────┬──────────────────────────────────────────┘
                           │
              ┌────────────▼────────────┐
              │   Ollama (deepseek-r1)  │
              │   or  Mock / NLP Mode   │
              └─────────────────────────┘
```

### Tech Stack

| Layer | Technology |
|:--|:--|
| **Frontend** | React 19, Vite 8, React Router 7, Recharts 3, Lucide Icons, Axios |
| **Backend** | Python 3.11+, FastAPI 0.115, Uvicorn, SQLAlchemy 2.0, Pydantic 2.9 |
| **AI / LLM** | Ollama (deepseek-r1:1.5b) — local inference, zero cloud dependency |
| **NLP Fallback** | scikit-learn TF-IDF + cosine similarity for conflict detection |
| **PDF Parsing** | PyMuPDF 1.24 |
| **Streaming** | Server-Sent Events (SSE) via sse-starlette |
| **Database** | SQLite (dev) / PostgreSQL (prod-ready) |

---

## Quick Start

### Prerequisites

| Tool | Version |
|:--|:--|
| Python | 3.11+ |
| Node.js | 18+ |
| Ollama | Latest _(optional — mock mode works without it)_ |

### 1. Clone the Repository

```bash
git clone https://github.com/DivyaMishra896/RegisterSync.git
cd RegisterSync
```

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
.\venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env if you want live LLM mode (see Configuration below)

# Generate sample RBI circular PDF
python generate_mock_pdf.py

# Start the API server
uvicorn main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 4. Open the App

| Service | URL |
|:--|:--|
| **Frontend** | [http://localhost:5173](http://localhost:5173) |
| **API Docs (Swagger)** | [http://localhost:8000/docs](http://localhost:8000/docs) |
| **API Docs (ReDoc)** | [http://localhost:8000/redoc](http://localhost:8000/redoc) |
| **Health Check** | [http://localhost:8000/api/health](http://localhost:8000/api/health) |

---

## Configuration

Copy `.env.example` → `.env` in the `backend/` directory:

```env
# ─── LLM Mode ───────────────────────────────────────
# "mock"  → No external dependencies, uses built-in mock data
# "live"  → Calls Ollama for real AI extraction
LLM_MODE=mock

# ─── Ollama Settings (only needed if LLM_MODE=live) ──
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=deepseek-r1:1.5b

# ─── Database ────────────────────────────────────────
DATABASE_URL=sqlite:///./suraksha.db

# ─── Frontend CORS ───────────────────────────────────
FRONTEND_URL=http://localhost:5173
```

> **Tip:** To use live AI extraction, install [Ollama](https://ollama.com), pull the model with `ollama pull deepseek-r1:1.5b`, and set `LLM_MODE=live`.

---

## API Reference

| Method | Endpoint | Description |
|:--|:--|:--|
| `POST` | `/api/upload` | Upload a PDF circular |
| `GET` | `/api/upload/circulars` | List all uploaded circulars |
| `GET` | `/api/extract/{id}/stream` | Stream AI extraction with SSE (agent thoughts + results) |
| `GET` | `/api/extract/{id}/rules` | Get extracted rules for a circular |
| `GET` | `/api/extract/{id}/conflicts` | Get detected conflicts for a circular |
| `GET` | `/api/tasks` | List tasks (filterable by `department`, `status`, `priority`, `circular_id`) |
| `GET` | `/api/tasks/stats` | Dashboard statistics, risk score, effort breakdown |
| `GET` | `/api/tasks/{id}` | Get a specific task |
| `PATCH` | `/api/tasks/{id}` | Update task status/owner/priority |
| `POST` | `/api/verify/run` | Run the verification agent |
| `GET` | `/api/verify/summary` | Get compliance verification summary |
| `GET` | `/api/health` | Health check |

Full interactive documentation available at [`/docs`](http://localhost:8000/docs) (Swagger UI).

---

## Project Structure

```
RegisterSync/
├── backend/
│   ├── main.py                          # FastAPI application entry point
│   ├── config.py                        # Environment & settings loader
│   ├── database.py                      # SQLAlchemy engine & session
│   ├── .env.example                     # Environment template
│   │
│   ├── models/
│   │   ├── circular.py                  # Circular ORM model
│   │   ├── rule.py                      # ExtractedRule ORM model
│   │   └── task.py                      # MAPTask ORM model
│   │
│   ├── routers/
│   │   ├── upload.py                    # PDF upload endpoints
│   │   ├── extraction.py                # AI extraction + SSE streaming
│   │   ├── tasks.py                     # Task CRUD + statistics
│   │   └── verification.py             # Verification agent endpoints
│   │
│   ├── services/
│   │   ├── agents/                      # 🤖 Multi-Agent System
│   │   │   ├── orchestrator.py          #    Pipeline coordinator
│   │   │   ├── base_agent.py            #    Abstract agent base class
│   │   │   ├── reader_agent.py          #    Document structure analyzer
│   │   │   ├── extractor_agent.py       #    Rule extraction specialist
│   │   │   ├── conflict_agent.py        #    Cross-regulation conflict detector
│   │   │   ├── router_agent.py          #    Department assignment agent
│   │   │   └── verifier_agent.py        #    Task verification agent
│   │   │
│   │   ├── llm_provider.py             # Ollama API client
│   │   ├── llm_extractor.py            # LLM extraction with mock fallback
│   │   ├── nlp_fallback.py             # TF-IDF based NLP fallback
│   │   ├── pdf_parser.py               # PyMuPDF text extraction & chunking
│   │   ├── map_generator.py            # Rule → MAPTask conversion
│   │   ├── department_router.py        # Keyword-based department routing
│   │   ├── department_data.py          # 440+ lines of Indian banking dept taxonomy
│   │   ├── conflict_checker.py         # Cosine similarity conflict detection
│   │   └── verification_agent.py       # Log-based compliance verification
│   │
│   ├── samples/                         # Sample RBI/SEBI circular PDFs
│   ├── mock_logs/                       # Mock SIEM/GRC logs for verification
│   ├── uploads/                         # User-uploaded PDFs (gitignored)
│   └── requirements.txt                # Python dependencies
│
├── frontend/
│   ├── index.html                       # App shell
│   ├── vite.config.js                   # Vite configuration
│   ├── package.json                     # Node dependencies
│   │
│   └── src/
│       ├── App.jsx                      # Router & layout setup
│       ├── main.jsx                     # React entry point
│       ├── index.css                    # Global styles & design system
│       │
│       ├── api/
│       │   └── client.js               # Axios API client
│       │
│       ├── components/
│       │   ├── Layout.jsx              # App shell with navigation
│       │   ├── UploadZone.jsx          # Drag-and-drop PDF upload
│       │   ├── ExtractionView.jsx      # SSE agent thought stream
│       │   ├── TaskBoard.jsx           # Task kanban board
│       │   ├── TaskCard.jsx            # Individual task card
│       │   ├── StatusBadge.jsx         # Status indicator component
│       │   ├── VerificationPanel.jsx   # Verification results display
│       │   └── ImpactPredictor.jsx     # Effort & risk charts
│       │
│       └── pages/
│           ├── UploadPage.jsx          # Upload + extraction flow
│           ├── DashboardPage.jsx       # Compliance dashboard
│           └── CircularsPage.jsx       # Circular management
│
├── .gitignore
└── README.md
```

---

## What Makes RegisterSync Different

### Multi-Agent Architecture
Unlike monolithic LLM calls, RegisterSync uses an **orchestrator pattern** with specialized agents — each with a focused role and system prompt. This produces more accurate, structured output than a single-shot extraction.

### The Verification Agent
While other compliance tools stop at task creation, RegisterSync **closes the loop**:
- Reads system logs (mock in prototype → real SIEM/GRC integration in production)
- Auto-verifies whether compliance tasks have actually been implemented
- Produces an audit trail with timestamps and evidence
- Calculates a dynamic **risk score** (0–100) based on task status, priority weights, and unresolved conflicts

### Indian Banking–Specific
The `department_data.py` module contains **440+ lines** of curated Indian banking department taxonomy covering:
- Digital Banking Services, Cybersecurity Wing, Risk Management
- RBI/SEBI/IRDAI regulatory mapping with advisory links
- Compliance Department, Internal Audit, IT Vertical, and more

### Zero Cloud Dependency
Runs entirely on-premise with **Ollama** for local LLM inference. No data ever leaves your network — critical for banking compliance workloads.

---

## Roadmap

- [ ] Production SIEM/GRC log integration for real verification
- [ ] PostgreSQL migration for production deployment
- [ ] Role-based access control (RBAC) for department-level views
- [ ] Email/Slack notifications for approaching deadlines
- [ ] Circular diff tracking (version-over-version comparison)
- [ ] PDF annotation with highlighted compliance sections
- [ ] Export compliance reports as PDF/Excel

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ for Indian Banking Compliance
</p>
