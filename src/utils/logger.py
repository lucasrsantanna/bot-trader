import logging
from config.settings import settings

def setup_logger():
    logger = logging.getLogger("bot_trader_ia")
    logger.setLevel(settings.LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console Handler
    ch = logging.StreamHandler()
    ch.setLevel(settings.LOG_LEVEL)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File Handler
    # fh = logging.FileHandler("bot_trader.log")
    # fh.setLevel(settings.LOG_LEVEL)
    # fh.setFormatter(formatter)
    # logger.addHandler(fh)

    return logger

logger = setup_logger()

