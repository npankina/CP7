import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name='app_logger', log_file='app.log', level=logging.INFO):
    """
    Настраивает логгер с заданным именем, файлом логов и уровнем логирования.
    """
    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Обработчик для записи логов в файл
    handler = RotatingFileHandler(log_file, maxBytes=100000, backupCount=1)
    handler.setLevel(level)

    # Формат логов
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    if not logger.handlers:
        logger.addHandler(handler)

    return logger
