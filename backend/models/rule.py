import json
from datetime import date
from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class ExtractedRule(Base):
    __tablename__ = "extracted_rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    circular_id = Column(Integer, ForeignKey("circulars.id"), nullable=False)
    rule_id = Column(String(20))
    title = Column(String(500))
    description = Column(Text)
    affected_departments = Column(Text, default="[]")
    deadline = Column(Date, nullable=True)
    priority = Column(String(20), default="Medium")
    estimated_effort_days = Column(Integer, default=7)
    has_conflict = Column(Boolean, default=False)
    conflict_details = Column(Text, default=None)

    circular = relationship("Circular", back_populates="rules")
    tasks = relationship("MAPTask", back_populates="rule", cascade="all, delete-orphan")

    def get_departments(self) -> list:
        try:
            return json.loads(self.affected_departments)
        except (json.JSONDecodeError, TypeError):
            return []

    def to_dict(self):
        return {
            "id": self.id,
            "circular_id": self.circular_id,
            "rule_id": self.rule_id,
            "title": self.title,
            "description": self.description,
            "affected_departments": self.get_departments(),
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "priority": self.priority,
            "estimated_effort_days": self.estimated_effort_days,
            "has_conflict": self.has_conflict,
            "conflict_details": json.loads(self.conflict_details) if self.conflict_details else None,
        }
