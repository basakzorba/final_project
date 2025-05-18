class quizcard:
    def __init__(self, term, definition):
        self.term = term
        self.definition = definition

    def check_answer(self, answer):
        # Compare the user's answer with the term (case-insensitive)
        return self.term.strip().lower() == answer.strip().lower()

    def get_term_and_definition(self):
        return self.term, self.definition