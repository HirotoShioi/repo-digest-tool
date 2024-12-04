# Configure logging
import logging


logging.basicConfig(
    filename="repo_tool.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_error(e: Exception):
    logging.error(str(e))
