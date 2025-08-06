# Logging
import logging
from pathlib import Path
from datetime import datetime

# Setup logs directory and log file path
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
log_file = log_dir/f"{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log"

# Configure handler
# console_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler(log_file, encoding="utf-8")
hand = [file_handler]

#Logging format
logging_str = "[%(asctime)s] [%(lineno)d] [%(name)s] - %(levelname)s - %(module)s: %(message)s"

        
# Basic Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format= logging_str,
    handlers=hand
)

