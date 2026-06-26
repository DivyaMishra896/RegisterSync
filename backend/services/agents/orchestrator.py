import json
from services.agents.reader_agent import ReaderAgent
from services.agents.extractor_agent import ExtractorAgent
from services.agents.conflict_agent import ConflictAgent
from services.agents.router_agent import RouterAgent

class OrchestratorAgent:
    def __init__(self):
        self.reader = ReaderAgent()
        self.extractor = ExtractorAgent()
        self.conflict = ConflictAgent()
        self.router = RouterAgent()

    async def run_extraction_pipeline(self, text_chunks: list, circular_id: int, existing_rules: list = None):
        if existing_rules is None:
            existing_rules = []
            
        combined_text = "\n\n".join(text_chunks)
        
        yield {
            "type": "thought",
            "agent": "Orchestrator",
            "thought": f"Starting extraction pipeline for Circular #{circular_id}."
        }
        
        yield {
            "type": "thought",
            "agent": "Reader",
            "thought": "Analyzing document structure and identifying regulatory sections..."
        }
        reader_result = await self.reader.analyze(combined_text)
        
        yield {
            "type": "thought",
            "agent": "Reader",
            "thought": f"Identified {len(reader_result.get('regulatory_sections', []))} regulatory sections. Subject: {reader_result.get('subject', 'Unknown')}."
        }
        
        yield {
            "type": "thought",
            "agent": "Extractor",
            "thought": "Extracting specific compliance rules, deadlines, and priorities..."
        }
        rules = await self.extractor.extract(reader_result.get('regulatory_sections', []))
        
        yield {
            "type": "thought",
            "agent": "Extractor",
            "thought": f"Successfully extracted {len(rules)} actionable rules."
        }
        
        if existing_rules:
            yield {
                "type": "thought",
                "agent": "Conflict",
                "thought": f"Comparing {len(rules)} new rules against existing regulatory database..."
            }
            conflicts = await self.conflict.find_conflicts(rules, existing_rules)
            yield {
                "type": "thought",
                "agent": "Conflict",
                "thought": f"Detected {len(conflicts)} potential conflicts or overlaps."
            }
        else:
            conflicts = []
            
        if rules:
            first_rule = rules[0]
            yield {
                "type": "thought",
                "agent": "Router",
                "thought": f"Routing rule '{first_rule.get('title')}'..."
            }
            router_res = await self.router.assign(first_rule.get("title", ""), first_rule.get("description", ""))
            yield {
                "type": "thought",
                "agent": "Router",
                "thought": f"Assigned to {', '.join(router_res.get('departments', []))} because: {router_res.get('reasoning', 'Standard routing')}."
            }
        
        yield {
            "type": "final_result",
            "data": {
                "rules": rules,
                "conflicts": conflicts
            }
        }
