import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "company_agent"))

from datetime import datetime
from app.database import SessionLocal
from app import models
from research_v2 import app as research_graph


def run_research_task(application_id: int):
    db = SessionLocal()
    try:
        app_obj = db.query(models.Application).filter(models.Application.id == application_id).first()
        if not app_obj:
            return

        app_obj.research_status = models.ResearchStatus.IN_PROGRESS
        db.commit()

        try:
            result = research_graph.invoke({"company_name": app_obj.company_name})
            app_obj.research_report = result["final_report"]
            app_obj.research_status = models.ResearchStatus.COMPLETED
            app_obj.research_generated_at = datetime.utcnow()
        except Exception as e:
            app_obj.research_status = models.ResearchStatus.FAILED
            app_obj.research_report = f"Research failed: {str(e)}"

        db.commit()
    finally:
        db.close()