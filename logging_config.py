import logging
from datetime import datetime
import os

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d")}.log')
    ]
)

logger = logging.getLogger('RAG_API_LOG')
