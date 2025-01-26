import logging
from pathlib import Path
from fastapi import HTTPException
from database import Database
from models import InterviewReportRequest
from storage import StorageManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Interview Manager
class ReportManager:
    def __init__(self):
        self.storage = StorageManager()
        self.db = Database()

    async def get_summary_report(self, request: InterviewReportRequest):
        if request.session_id is None:
            raise HTTPException(status_code=404, detail="session_id in request is empty")

        file_path = f"{self.storage.path}/{request.session_id}.json"

        if Path(file_path).exists() is False:
            raise HTTPException(status_code=404, detail="Report not exist")

        report = await self.storage.read_interview_data(file_path)
        return report

    async def get_session_log(self):
        data=await self.db.get_all_logs()
        return await self.db.get_log_data(data)



