import json
from flashcard import flashcard

class FlashcardManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.flashcards = self.load_flashcards()
    
    def load_flashcards(self):
        # Load questions from the JSON file
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return [flashcard(item["term"], item["definition"]) for item in data]