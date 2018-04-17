from flask import json


class Config(object):
    def __init__(self, file_name: str):
        self._file_name = file_name

        try:
            with open(file_name, 'r') as f:
                data = json.load(f)
                self.last_weight = data['previous_weight']
        except FileNotFoundError:
            self.last_weight = None

    def set_weight(self, weight: float):
        self.last_weight = weight

        with open(self._file_name, 'w') as f:
            json.dump(self.to_dict(), f)

    def to_dict(self) -> dict:
        return {'previous_weight': self.last_weight}
