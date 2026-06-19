"""
MAPTask model — Measurable Action Point generated from an extracted rule.
"""

import json
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class MAPTask(Base):
    __tablename__ = "map_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_id = Column(Integer, ForeignKey("extracted_rules.id"), nullable=True)
    circular_id = Column(Integer, ForeignKey("circulars.id"), nullable=False)
    task_ref = Column(String(20))  # "MAP-001"
    title = Column(String(500))
    description = Column(Text)
    department = Column(String(100))  # IT Security, Risk Management, Operations
    priority = Column(String(20), default="Medium")
    deadline = Column(Date, nullable=True)
    status = Column(String(50), default="Pending")  # Pending, Verified, Failed, Partially Done
    owner = Column(String(200), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)
    evidence_link = Column(String(500), nullable=True)
    audit_trail = Column(Text, default="[]")  # JSON array of verification events
    sub_vertical = Column(String(200), default="")      # Sub-vertical assignment
    regulator = Column(String(100), default="")          # Primary regulator (RBI, CERT-In, etc.)
    advisory = Column(String(500), default="")           # Specific advisory/regulation name
    routing_reason = Column(Text, default="")            # Why this dept was assigned

    # Relationships
    rule = relationship("ExtractedRule", back_populates="tasks")
    circular = relationship("Circular", back_populates="tasks")

    def get_audit_trail(self) -> list:
        try:
            return json.loads(self.audit_trail)
        except (json.JSONDecodeError, TypeError):
            return []

    def add_audit_event(self, event: dict):
        trail = self.get_audit_trail()
        trail.append(event)
        self.audit_trail = json.dumps(trail)

    def to_dict(self):
        return {
            "id": self.id,
            "rule_id": self.rule_id,
            "circular_id": self.circular_id,
            "task_ref": self.task_ref,
            "title": self.title,
            "description": self.description,
            "department": self.department,
            "priority": self.priority,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "status": self.status,
            "owner": self.owner,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "verified_at": self.verified_at.isoformat() if self.verified_at else None,
            "evidence_link": self.evidence_link,
            "audit_trail": self.get_audit_trail(),
            "sub_vertical": self.sub_vertical,
            "regulator": self.regulator,
            "advisory": self.advisory,
            "routing_reason": self.routing_reason,
        }
