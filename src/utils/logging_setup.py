import logging
import os
from datetime import datetime

def setup_logger(run_name: str = None, output_dir: str = None) -> tuple[logging.Logger, str]:
    """
    Sets up a logger that writes to a timestamped log file inside `logs` subfolder of output_dir.
    If output_dir is None, defaults to logs/run_timestamp folder.

    Returns logger and the log directory path.
    """
    if output_dir is None:
        # Default logs folder if output_dir not provided
        ROOT_LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        run_folder = run_name or f"run_{timestamp}"
        RUN_LOG_DIR = os.path.join(ROOT_LOG_DIR, run_folder)
    else:
        # Logs go inside the `logs` subfolder of output_dir
        RUN_LOG_DIR = os.path.join(output_dir, "logs")

    os.makedirs(RUN_LOG_DIR, exist_ok=True)

    # New log file per run, with timestamp in filename:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"log-{timestamp}.log"
    LOG_FILE = os.path.join(RUN_LOG_DIR, log_filename)

    # Clear existing handlers if any, to prevent duplicate logs if called multiple times
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler()  
        ]
    )

    logger = logging.getLogger("YouTubeStoryGenerator")
    logger.info(f"Logger initialized. Logs directory: {RUN_LOG_DIR}")
    logger.info(f"Log file: {LOG_FILE}")
    return logger, RUN_LOG_DIR
