from datetime import datetime

from config.settings import settings
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    logger.info("=" * 50)
    logger.info(f"Project : {settings.PROJECT_NAME}")
    logger.info(f"Version : {settings.VERSION}")
    logger.info(f"Started : {datetime.now()}")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()