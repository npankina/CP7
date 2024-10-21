import os
import json

class DataAdapter:
    def __init__(self, source_type='json', source_path='data/products.json'):
        self.source_type = source_type
        self.source_path = source_path

    def load_data(self):
        if self.source_type == 'json':
            return self._load_from_json()
        elif self.source_type == 'db':
            return self._load_from_db()
        else:
            raise ValueError(f"Unsupported source type: {self.source_type}")

    def save_data(self, data):
        if self.source_type == 'json':
            self._save_to_json(data)
        elif self.source_type == 'db':
            self._save_to_db(data)
        else:
            raise ValueError(f"Unsupported source type: {self.source_type}")

    def _load_from_json(self):
        if os.path.exists(self.source_path):
            with open(self.source_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        return []

    def _save_to_json(self, data):
        with open(self.source_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def _load_from_db(self):
        # Заглушка для загрузки из БД
        return []

    def _save_to_db(self, data):
        # Заглушка для сохранения в БД
        pass
#----------------------------------------------------------------------------------------------------