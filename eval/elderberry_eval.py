from core import FructoseEval
class ElderberryEval(FructoseEval):
    @staticmethod
    def eval_get_avg_len(yeet):
        @yeet(debug=True)
        def get_avg_len(words: list[str]) -> int:
          """
          Calculates the average length of the words in a given list.
          """

        get_avg_len(["dog","window","skyscraper"])

    @staticmethod
    def eval_get_theme(yeet):
        @yeet(debug=True)
        def get_theme(words: list[str]) -> str:
          """
          Figures out a single common theme for the given list of words.
          """

        get_theme(["dog","window","purple"])

    @staticmethod
    def eval_choose_word(yeet):
        @yeet(debug=True)
        def choose_word() -> str:
          """
          Chooses a random word for the user to guess in a hangman game. The list of words can be anything, however varied. And obscure words are preferred. The categories can be anything and mixed.
          """

        choose_word()

    @staticmethod
    def eval_choose_words(yeet):
        @yeet(debug=True)
        def choose_words(n: int) -> list[str]:
          """
          Chooses n random words for the user to guess in a hangman game. The list of words can be anything, however varied. Prefers obscure words. The categories can be anything and mixed.
          """

        choose_words(2)

    @staticmethod
    def eval_guess_letter(yeet):
        @yeet(debug=True)
        def guess_letter(word: str, letter: str) -> bool:
          """
          Checks if the letter is in the word.
          """

        guess_letter("xertz", "t")

    @staticmethod
    def eval_generate_data(yeet):
        @yeet(debug=True)
        def generate_data(schema: str) -> dict:
          """
          Generates data based on the given schema.
          """

        generate_data("name:str,age:int,city:str")

