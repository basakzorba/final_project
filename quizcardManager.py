import json
from quizcard import quizcard

class QuizcardManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.quizcards = self.load_quizcards()
    
    def load_quizcards(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [quizcard(item["term"], item["definition"]) for item in data]
        except FileNotFoundError:
            print(f"Error: JSON File '{self.file_path}' was not found")
            return []
