import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Database configuration
# SQLite is now the default database
USE_SQLITE = True  # Set to True to use SQLite, False for MySQL

# MySQL configuration (only used if USE_SQLITE = False)
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'username',  # Replace with your MySQL username
    'password': 'password',  # Replace with your MySQL password
    'database': 'family_budget',
    'port': 3306,  # Default MySQL port (change if needed)
    'connect_timeout': 10,  # Connection timeout in seconds
    'raise_on_warnings': True
}

# SQLite configuration
SQLITE_DB_FILE = 'family_budget.db'

# Telegram Bot Token
TELEGRAM_TOKEN = os.getenv('BOT_TOKEN')

# Conversation states
MAIN_MENU, ADD_RECORD, SELECT_CATEGORY, ENTER_AMOUNT, CONFIRM_RECORD, GENERATE_REPORT = range(6)
