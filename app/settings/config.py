from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent.parent

load_dotenv(PROJECT_ROOT / '.env')

DB_URL = 'postgresql://admin:1234@172.22.58.152:5432/missions_db'
