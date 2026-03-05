from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True)
    script_name = Column(String, nullable=False)
    script_type = Column(String, nullable=False)

    start_time = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
        )
    end_time = Column(DateTime(timezone=True))
    duration = Column(Float)

    status = Column(String)
    exit_code = Column(Integer)

    avg_cpu = Column(Float)
    max_cpu = Column(Float)
    avg_mem = Column(Float)
    max_mem = Column(Float)
    avg_gpu = Column(Float)

    stdout = Column(Text)
    stderr = Column(Text)
