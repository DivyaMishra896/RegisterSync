"""
Circular model — represents an uploaded regulatory PDF document.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from database import Base


class Circular(Base):
    __tablename__ = "circulars"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    source = Column(String(50), default="RBI")  # RBI, SEBI, etc.
    raw_text = Column(Text, default="")
    status = Column(String(50), default="uploaded")  # uploaded, extracting, extracted, processed

    # Relationships
    rules = relationship("ExtractedRule", back_populates="circular", cascade="all, delete-orphan")
    tasks = relationship("MAPTask", back_populates="circular", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "upload_date": self.upload_date.isoformat() if self.upload_date else None,
            "source": self.source,
            "raw_text": self.raw_text,
            "status": self.status,
            "rule_count": len(self.rules) if self.rules else 0,
            "task_count": len(self.tasks) if self.tasks else 0,
        }
