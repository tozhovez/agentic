
import asyncio
import json

import logging
import aiosqlite
from models import InterviewSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path="interviews.db"):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS interview_sessions (
                    session_id TEXT PRIMARY KEY,
                    candidate_id TEXT,
                    job_title TEXT,
                    timestamp TEXT,
                    data_path TEXT
                )
            """)
            await db.commit()

    async def save_session(self, session: InterviewSession):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO interview_sessions (session_id, candidate_id, job_title, timestamp, data_path)
                VALUES (?, ?, ?, ?, ?)
            """, (
                session.session_id,
                session.candidate_id,
                session.job_title,
                session.timestamp,
                session.data_path
                ))
            await db.commit()


    async def get_all_logs(self):
        """Retrieve all logs from the SQLite database."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT session_id, candidate_id, job_title, timestamp, data_path
                FROM interview_sessions
                """) as cursor:
                logs = await cursor.fetchall()
        return logs



    async def get_logs_by_candidate(self, candidate_id):
        """Retrieve logs for a specific candidate."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT * FROM interview_sessions WHERE candidate_id = ?", (candidate_id,)
            ) as cursor:
                logs = await cursor.fetchall()
        return logs

    async def get_log_data(self, data):
        fields = ["session_id", "candidate_id", "job_title", "timestamp", "data_path"]
        log = [dict(zip(fields, row)) for row in data]
        data = json.dumps(log)
        return data

async def main():
    db = Database()
    data = await db.get_all_logs()
    await db.get_log_data(data)


if __name__ == '__main__':
    asyncio.run(main())
