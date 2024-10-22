import logging
import os

# Получаем текущую рабочую директорию
log_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_dir, 'application.log')

# Настройка логгера для всего приложения
logger = logging.getLogger("ApplicationLogger")
logger.setLevel(logging.INFO)

# Создание обработчика для записи в файл
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setLevel(logging.INFO)

# Форматирование логов
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
if not logger.handlers:
    logger.addHandler(file_handler)
