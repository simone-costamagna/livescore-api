import logging
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG') == 'True'


def configure_logging():
    """
    Set up logging configuration defining log format, level, and output.
    """
    logging.basicConfig(
        level=logging.DEBUG if DEBUG else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler()],
    )