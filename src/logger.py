import logging
from src.config import config

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger(__name__)

# Suppress logs from other libraries
libraries = [
]

for lib in libraries:
    logging.getLogger(lib).setLevel(logging.WARNING)
