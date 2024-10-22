import os

class Config:
    """Базовая конфигурация приложения"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # Секретный ключ по умолчанию
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключение уведомлений об изменениях в модели

class Development_Config(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DEV_DATABASE_URI',
        'postgresql://shop_admin:0000@localhost:5432/shop_db'
    )

class Production_Config(Config):
    """Конфигурация для продакшена"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')  # URI берется из переменной окружения

class Testing_Config(Config):
    """Конфигурация для тестирования"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'TEST_DATABASE_URI',
        'postgresql://shop_admin:0000@localhost:5432/test_shop_db'
    )
    # В тестовой базе можно добавить настройку для быстрого отката транзакций
    SQLALCHEMY_ENGINE_OPTIONS = {'poolclass': 'StaticPool', 'connect_args': {'check_same_thread': False}}

# Словарь для выбора конфигурации
config_by_name = {
    'development': Development_Config,
    'production': Production_Config,
    'testing': Testing_Config
}
