import logging
import logging.handlers

def get_logger(name):
    # Step 1: Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Step 2: Create handlers
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # File handler
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.INFO)

    # Rotating file handler
    rotating_handler = logging.handlers.RotatingFileHandler(
        'app_rotating.log', maxBytes=1024*1024, backupCount=3)
    rotating_handler.setLevel(logging.WARNING)

    # Step 3: Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Step 4: Attach the formatter to the handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    rotating_handler.setFormatter(formatter)

    # Step 5: Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(rotating_handler)

    return logger


