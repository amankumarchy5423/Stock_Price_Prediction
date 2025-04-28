import logging
import os
from datetime import datetime
from src.Common import common_variable



logging_dir = common_variable.LOGGING_DIR
logging_file = f"{datetime.now().strftime("%d/%m/%Y//%H:%M:%S")}.log"

log_file = os.path.join(logging_dir,logging_file)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    filename=log_file
)

my_log = logging.getLogger("<< STOCK PRICE PRIDICTION >>")