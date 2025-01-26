from pathlib import  Path
import json
import logging
import aiofiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StorageManager:
    def __init__(self, file_path="local_storage"):
        self.path = file_path
        Path(self.path).mkdir(mode=0o777, parents=False, exist_ok=True)

    async def save_interview_data(self, filename: str, data: dict):
        """Save interview data to local storage asynchronously."""
        async with aiofiles.open(filename, mode='w') as f:
            await f.write(json.dumps(data, indent=2))

    async def read_interview_data(self, filename: str):
        """Save interview data to local storage asynchronously."""
        async with aiofiles.open(filename, mode='r') as f:
            return json.loads(await f.read())
    
    


