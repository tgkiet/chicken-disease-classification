import os 
import sys
import logging

logging_str = "[%(asctime)s]: %(levelname)s: %(module)s: %(message)s]"

log_dir = "logs"
log_filepath = os.path.join(log_dir, "running_logs.log")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO, # từ cấp độ INFO trở lên sẽ được ghi lại
    format=logging_str, # định dạng của log
    
    handlers=[
        logging.FileHandler(log_filepath), # Log to file (log_filepath)
        logging.StreamHandler(sys.stdout) # log to terminal (stdout: standard output)
    ]
)

logger = logging.getLogger("cnnClassifierLogger") # Tạo logger với tên "cnnClassifierLogger"