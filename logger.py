import logging
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)

log_filename = os.path.join("logs", f"{datetime.now().strftime('%d-%m-%Y')}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S-%d.%m.%Y",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_filename, encoding="utf-8"),
    ],
    force=True,
)

logging.getLogger("TeleBot").setLevel(logging.ERROR)

logger = logging.getLogger("bot")
logger.setLevel(logging.DEBUG)