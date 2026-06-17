# Agentic Architecture Overhaul: Multi-Agent System with Swappable Local LLM

## Background

**Hackathon theme**: *"Agentic Regulatory Intelligence & Compliance — Build an Agentic system that monitors regulatory changes, translates them into MAPs, assigns them to the correct bank departments, and autonomously validates completion."*

**Constraint**: No outside LLM API. Solution must run without internet.

**Current state**: Fixed pipeline calling Gemini API (or returning hardcoded mock). Not agentic.

**Goal**: Transform Suraksha into a **true multi-agent system** where AI agents reason, decide, and act autonomously — powered by a local LLM via Ollama, with the model easily swappable via a single config variable.

---

## User Review Required

> [!IMPORTANT]
> **Model Swappability**: The model will be configurable via a single env var `OLLAMA_MODEL=phi3:mini`. To swap models, your teammate just changes this to `mistral`, `gemma2:2b`, `llama3`, etc. No code changes needed.

> [!IMPORTANT]
> **Dual-mode development**: You develop on your laptop using `LLM_MODE=mock` (regex fallback, fast). Your teammate demos on the Victus with `LLM_MODE=ollama` (real AI, GPU-accelerated). Same codebase, just one env var toggle.

> [!WARNING]
> **Database reset**: Since we're changing how rules are extracted (real analysis vs hardcoded), the existing `suraksha.db` will need to be deleted and recreated. This is fine since it only has mock data.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   ORCHESTRATOR AGENT                     │
│  Coordinates the pipeline, decides next steps,           │
│  handles errors, produces reasoning trail                │
│                                                          │
│  Tools: reader_agent, extractor_agent, conflict_agent,   │
│         router_agent, verifier_agent                     │
└──────────┬──────────────────────────────────────────────┘
           │ Step 1: "Let me read this circular"
           ▼
┌──────────────────┐     ┌───────────────────┐
│   READER AGENT   │────→│  EXTRACTOR AGENT  │
│  Sections, type, │     │  Rules, deadlines, │
│  subject matter  │     │  priorities        │
└──────────────────┘     └────────┬──────────┘
                                  │ Step 3: "Check for conflicts"
                    ┌─────────────┼──────────────┐
                    ▼             ▼              ▼
          ┌──────────────┐ ┌───────────┐ ┌──────────────┐
          │CONFLICT AGENT│ │ROUTER AGT │ │VERIFIER AGENT│
          │Compare old vs│ │Dept assign│ │Check logs    │
          │new rules     │ │with reason│ │prove done    │
          └──────────────┘ └───────────┘ └──────────────┘
```

Each agent call produces a **reasoning trace** visible in the UI.

---

## Proposed Changes

### Component 1: LLM Provider (Swappable)

#### [NEW] [llm_provider.py](file:///c:/Users/hp/Desktop/Suraksha/backend/services/llm_provider.py)

A unified LLM interface that supports multiple backends. **Swapping models is a single env var change.**

```python
# Configuration:
#   OLLAMA_MODEL=phi3:mini       ← swap to mistral, gemma2:2b, llama3, etc.
#   OLLAMA_URL=http://localhost:11434
#   LLM_MODE=ollama              ← or "mock" for dev without Ollama
```

### Component 1b: SSE Streaming (Score Booster)
To show the agents thinking in real-time, we will use **Server-Sent Events (SSE)**.
- As each agent in the Orchestrator finishes a thought, it yields a JSON string.
- FastAPI will stream this via `EventSourceResponse`.
- The React frontend will display the thoughts live with a typing effect.

```python
class LLMProvider:
    """Unified interface — swap models without touching code."""
    
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        if mode == "ollama":
            # POST to http://localhost:11434/api/generate
            # model = config.OLLAMA_MODEL  ← swappable!
        elif mode == "mock":
            # Regex-based NLP fallback for development
```

**Key design**:
- `OLLAMA_MODEL` env var controls which model runs — no code changes to swap
- `OLLAMA_URL` defaults to `http://localhost:11434` (Ollama's default)
- `LLM_MODE` toggles between `ollama` and `mock`
- All agent code calls `llm_provider.generate()` — never talks to Ollama directly
- Includes timeout handling, retry logic, JSON parsing with fallback

---

### Component 2: Agent Framework

#### [NEW] [agents/base_agent.py](file:///c:/Users/hp/Desktop/Suraksha/backend/services/agents/base_agent.py)

Base class for all agents:

```python
class BaseAgent:
    name: str                    # e.g. "Reader Agent"
    role: str                    # System prompt describing the agent's role
    reasoning_log: list[dict]    # Visible reasoning trail
    
    async def think(self, context: str) -> dict:
        """Call LLM with agent's system prompt, return structured output."""
        # Logs reasoning: {"agent": "Reader", "thought": "...", "action": "...", "result": "..."}
    
    async def act(self, action: str, **kwargs) -> dict:
        """Execute a tool/action based on the agent's decision."""
```

Every agent call appends to `reasoning_log`, which gets streamed to the frontend.

---

#### [NEW] [agents/reader_agent.py](file:///c:/Users/hp/Desktop/Suraksha/backend/services/agents/reader_agent.py)

**Role**: Analyze PDF text, identify regulatory sections, summarize the document.

**System prompt**: *"You are a regulatory document analyst for Indian banking. Given raw text from an RBI/SEBI circular, identify: (1) the circular's subject and reference number, (2) which sections contain mandatory regulatory requirements vs informational context, (3) a brief summary. Respond in JSON."*

**Output**: `{ subject, reference, summary, regulatory_sections: [...], info_sections: [...] }`

**Mock fallback**: Basic regex to split text into sections using numbered headings and regulatory keywords.

---

#### [NEW] [agents/extractor_agent.py](file:///c:/Users/hp/Desktop/Suraksha/backend/services/agents/extractor_agent.py)

**Role**: Extract structured rules from regulatory sections.

**System prompt**: *"You are a compliance rules extractor. Given regulatory text sections from an Indian banking circular, extract each distinct regulatory requirement as a structured rule. For each rule provide: rule_id, title, description, affected_departments (from: IT Security, Risk Management, Operations), deadline, priority (Critical/High/Medium/Low), estimated_effort_days. Respond in JSON: {rules: [...]}."*

**Output**: Same format as current `MOCK_EXTRACTION_RESPONSE` — **so the rest of the pipeline (MAP generator, DB models) doesn't change at all.**

**Mock fallback**: Regex sentence filtering (same as the NLP engine we designed earlier — regulatory keyword matching, entity extraction, priority scoring).

---

#### [NEW] [agents/conflict_agent.py](file:///c:/Users/hp/Desktop/Suraksha/backend/services/agents/conflict_agent.py)

**Role**: Compare new rules against existing rules, find contradictions.

**System prompt**: *"You are a regulatory conflict analyst. Compare NEW rules against EXISTING rules and identify conflicts. For each conflict: classify as CONTRADICTS, SUPERSEDED, or OVERLAPS, assign severity, and explain your reasoning. Respond in JSON: {conflicts: [...]}."*

**Output**: Same format as current `MOCK_CONFLICT_RESULTS`.

**Mock fallback**: TF-IDF cosine similarity + keyword contradiction detection (scikit-learn). Uses existing `MOCK_EXISTING_RULES` as the historical rule base.

---

#### [NEW] [agents/router_agent.py](file:///c:/Users/hp/Desktop/Suraksha/backend/services/agents/router_agent.py)

**Role**: Assign rules to departments with reasoning.

**System prompt**: *"You are a compliance task router for an Indian bank. Given a regulatory rule, determine which departments should handle it and explain why. Departments: IT Security, Risk Management, Operations."*

**Output**: `{ department: [...], reasoning: "..." }`

**Mock fallback**: Existing keyword-based `department_router.py` logic (already works well).

---

#### [NEW] [agents/verifier_agent.py](file:///c:/Users/hp/Desktop/Suraksha/backend/services/agents/verifier_agent.py)

**Role**: Check system logs to verify task completion. **This stays mostly the same** since it already reads actual log files — it's already the most "agentic" part. We enhance it with LLM reasoning:

**System prompt**: *"You are a compliance verification agent. Given a task description and a system log entry, determine if the log entry proves the task was completed. Classify as: Verified (clear evidence), Partially Done (some evidence), Failed (contradictory evidence), or No Evidence. Explain your reasoning."*

**Mock fallback**: Existing log-matching logic in `verification_agent.py`.

---

#### [NEW] [agents/orchestrator.py](file:///c:/Users/hp/Desktop/Suraksha/backend/services/agents/orchestrator.py)

**Role**: Coordinates all agents in sequence, makes decisions, produces the full reasoning trail.

```python
class OrchestratorAgent:
    async def run_pipeline(self, circular_text: str, circular_id: int, db: Session) -> dict:
        reasoning_log = []
        
        # Step 1: Reader Agent
        reasoning_log.append({"agent": "Orchestrator", "thought": "Received new circular. Starting analysis..."})
        reader_result = await self.reader_agent.think(circular_text)
        reasoning_log.append({"agent": "Reader", "thought": reader_result["summary"], ...})
        
        # Step 2: Extractor Agent  
        reasoning_log.append({"agent": "Orchestrator", "thought": f"Found {len(sections)} regulatory sections. Extracting rules..."})
        rules = await self.extractor_agent.think(reader_result["regulatory_sections"])
        
        # Step 3: Conflict Agent
        reasoning_log.append({"agent": "Orchestrator", "thought": f"Extracted {len(rules)} rules. Checking for conflicts..."})
        conflicts = await self.conflict_agent.think(rules, existing_rules)
        
        # Step 4: Decision point — if critical conflicts found, flag for review
        if any(c["severity"] == "High" for c in conflicts):
            reasoning_log.append({"agent": "Orchestrator", "thought": "⚠️ High-severity conflict detected! Flagging for manual review."})
        
        # Step 5: Router Agent — assign departments
        # Step 6: Generate MAPs
        # Step 7: Return everything with full reasoning trail
        
        return {
            "rules": ..., "tasks": ..., "conflicts": ...,
            "reasoning_log": reasoning_log  # ← this is what makes it "agentic"
        }
```

---

### Component 3: Modify Existing Backend Files

#### [MODIFY] [config.py](file:///c:/Users/hp/Desktop/Suraksha/backend/config.py)

```diff
- GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
- LLM_MODE: str = os.getenv("LLM_MODE", "mock")
+ LLM_MODE: str = os.getenv("LLM_MODE", "mock")       # "ollama" or "mock"
+ OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
+ OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "phi3:mini")  # ← SWAP MODELS HERE
```

#### [MODIFY] [.env.example](file:///c:/Users/hp/Desktop/Suraksha/backend/.env.example)

```env
# LLM Configuration
# Set to "ollama" for local AI (requires Ollama running)
# Set to "mock" for development (regex-based fallback, no AI needed)
LLM_MODE=mock

# Ollama Configuration (only needed if LLM_MODE=ollama)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=phi3:mini
# Other options: mistral, gemma2:2b, llama3, tinyllama

# Database (SQLite for offline use)
DATABASE_URL=sqlite:///./suraksha.db

# Frontend CORS
FRONTEND_URL=http://localhost:5173
```

#### [MODIFY] [requirements.txt](file:///c:/Users/hp/Desktop/Suraksha/backend/requirements.txt)

```diff
- google-genai>=1.0.0
+ httpx>=0.27.0          # async HTTP client for Ollama API
+ scikit-learn>=1.5.0    # TF-IDF for mock-mode conflict detection
```

#### [MODIFY] [llm_extractor.py](file:///c:/Users/hp/Desktop/Suraksha/backend/services/llm_extractor.py)

Rewrite to delegate to the Orchestrator Agent instead of calling Gemini directly. The function signature and return format stay the same so [extraction.py](file:///c:/Users/hp/Desktop/Suraksha/backend/routers/extraction.py) doesn't need changes.

```python
async def extract_rules_from_text(text_chunks, circular_id):
    orchestrator = OrchestratorAgent()
    result = await orchestrator.run_extraction(text_chunks, circular_id)
    return result  # Same format: {"rules": [...]}
```

#### [MODIFY] [conflict_checker.py](file:///c:/Users/hp/Desktop/Suraksha/backend/services/conflict_checker.py)

Delegate to Conflict Agent. Keep mock existing rules for demo. The return format stays the same.

#### [MODIFY] [extraction.py](file:///c:/Users/hp/Desktop/Suraksha/backend/routers/extraction.py) (router)

Add SSE streaming endpoint for real-time agent reasoning:

```python
@router.get("/{circular_id}/stream")
async def extract_rules_stream(circular_id: int, db: Session = Depends(get_db)):
    # Returns an EventSourceResponse that streams agent thoughts
```

#### [MODIFY] [tasks.py](file:///c:/Users/hp/Desktop/Suraksha/backend/routers/tasks.py) (router)
Add a new endpoint for the **Compliance Risk Score**:
- Calculates risk based on pending tasks, unverified tasks, and unresolved conflicts.

---

### Component 4: Frontend — Score Boosters

#### [MODIFY] [ExtractionView.jsx](file:///c:/Users/hp/Desktop/Suraksha/frontend/src/components/ExtractionView.jsx)

Add the **Agent Reasoning Log** with SSE streaming:
- Connects to `/api/extract/{id}/stream`
- Displays thoughts as they arrive, mimicking a live terminal.

#### [MODIFY] [DashboardPage.jsx](file:///c:/Users/hp/Desktop/Suraksha/frontend/src/pages/DashboardPage.jsx)
- Add **Compliance Risk Score** card (e.g., "73/100 - HIGH RISK").

#### [NEW] Regulatory Diff View Component
- A side-by-side visual diff component for when the Conflict Agent detects a conflict between an old and new rule.

Add an **"Agent Reasoning Log"** panel that shows each agent's thinking in real-time during extraction. This is the **"wow factor"** for judges:

```
┌─────────────────────────────────────────────────────┐
│  🤖 Agent Reasoning Log                            │
├─────────────────────────────────────────────────────┤
│  🎯 Orchestrator: "Received RBI Circular. Starting  │
│     analysis pipeline..."                           │
│  📖 Reader Agent: "Identified 5 regulatory sections │
│     and 3 informational sections. Subject: Cyber    │
│     Security Framework for Banks."                  │
│  🔍 Extractor Agent: "Extracted 6 rules. R-003 has  │
│     'within 6 hours' deadline → marking Critical."  │
│  ⚡ Conflict Agent: "R-001 conflicts with HIST-001.  │
│     Reason: New rule relaxes VAPT from quarterly to │
│     semi-annual."                                   │
│  📋 Router Agent: "R-003 → IT Security (cyber       │
│     incident, CSOC) + Risk Management (risk         │
│     assessment)."                                   │
│  ✅ Done: 6 rules extracted, 8 MAPs generated,       │
│     2 conflicts detected.                           │
└─────────────────────────────────────────────────────┘
```

This will be styled as a terminal-like log with animated typing effect and agent-colored icons.

---

### Component 5: New Files Summary

```
backend/services/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Base class with reasoning log
│   ├── orchestrator.py        # Coordinates all agents
│   ├── reader_agent.py        # PDF text analysis
│   ├── extractor_agent.py     # Rule extraction
│   ├── conflict_agent.py      # Conflict detection
│   ├── router_agent.py        # Department routing
│   └── verifier_agent.py      # Log verification (enhanced)
├── llm_provider.py            # Unified LLM interface (Ollama/mock)
├── nlp_fallback.py            # Regex/TF-IDF fallback for mock mode
├── llm_extractor.py           # MODIFIED — delegates to orchestrator
├── conflict_checker.py        # MODIFIED — delegates to conflict agent
├── department_router.py       # Unchanged (used by router agent fallback)
├── map_generator.py           # Unchanged
├── pdf_parser.py              # Unchanged
└── verification_agent.py      # MODIFIED — enhanced with LLM reasoning
```

---

## What Stays The Same (No Changes Needed)

These files work as-is and don't need modification:

| File | Why it's fine |
|---|---|
| [pdf_parser.py](file:///c:/Users/hp/Desktop/Suraksha/backend/services/pdf_parser.py) | Already extracts text from PDFs correctly |
| [map_generator.py](file:///c:/Users/hp/Desktop/Suraksha/backend/services/map_generator.py) | Takes rules → creates MAPs. Input format unchanged |
| [department_router.py](file:///c:/Users/hp/Desktop/Suraksha/backend/services/department_router.py) | Used as fallback in mock mode |
| [models/](file:///c:/Users/hp/Desktop/Suraksha/backend/models) | All DB models stay the same |
| [routers/upload.py](file:///c:/Users/hp/Desktop/Suraksha/backend/routers/upload.py) | Upload flow unchanged |
| [routers/tasks.py](file:///c:/Users/hp/Desktop/Suraksha/backend/routers/tasks.py) | Task CRUD unchanged |
| [routers/verification.py](file:///c:/Users/hp/Desktop/Suraksha/backend/routers/verification.py) | Verification endpoints unchanged |
| [database.py](file:///c:/Users/hp/Desktop/Suraksha/backend/database.py) | DB setup unchanged |
| [main.py](file:///c:/Users/hp/Desktop/Suraksha/backend/main.py) | App entry unchanged |
| Frontend pages/components | Mostly unchanged (only ExtractionView gets the reasoning panel) |

---

## Model Swapping — How It Works

Your teammate runs:
```bash
# Default (recommended for RTX 3050 with 4GB VRAM)
OLLAMA_MODEL=phi3:mini

# Want to try Mistral? Just change the env var:
OLLAMA_MODEL=mistral

# Smaller/faster option:
OLLAMA_MODEL=gemma2:2b

# Tiny for testing:
OLLAMA_MODEL=tinyllama
```

**No code changes.** The `LLMProvider` reads `OLLAMA_MODEL` from config and passes it to every Ollama API call.

To pull a new model:
```bash
ollama pull mistral    # downloads once, ~4GB
ollama pull phi3:mini  # downloads once, ~2.3GB
```

---

## Verification Plan

### Automated Tests
```bash
# 1. Test mock mode (your laptop — no Ollama needed)
cd backend
set LLM_MODE=mock
uvicorn main:app --reload
# Upload a PDF → verify regex-based extraction works
# Check reasoning log shows agent steps

# 2. Test Ollama mode (teammate's Victus)
set LLM_MODE=ollama
set OLLAMA_MODEL=phi3:mini
ollama serve  # in a separate terminal
uvicorn main:app --reload
# Upload same PDF → verify LLM-based extraction works
# Check reasoning log shows real AI reasoning
```

### Manual Verification
1. Upload a **new** RBI circular PDF (not the mock one) → verify rules are extracted from actual text
2. Swap model from `phi3:mini` to `gemma2:2b` → verify everything still works with zero code changes
3. Disconnect internet → verify everything runs offline
4. Check the **Agent Reasoning Log** panel shows clear thinking for each agent
5. Demo the full flow: Upload → Agents Think → Dashboard → Conflicts → Verification

### Demo Day Checklist
- [ ] Ollama installed on Victus laptop
- [ ] `phi3:mini` model pulled
- [ ] Backend running with `LLM_MODE=ollama`
- [ ] Frontend showing agent reasoning panel
- [ ] 2-3 sample RBI circular PDFs ready for upload
- [ ] Internet disconnected to prove offline capability
