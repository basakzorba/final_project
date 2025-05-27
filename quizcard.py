class quizcard:
    def __init__(self, term, definition):
        self.term = term
        self.definition = definition

    def check_answer(self, answer):
        if answer.lower() == self.term.lower():
            return True
        return False

    def get_term_and_definition(self):
        return self.term, self.definition