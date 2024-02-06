from core import FructoseEval
from dataclasses import dataclass

@dataclass
class House:
  color: str
  size: int
  is_occupied: bool 


@dataclass
class Player:
  hp: int
  def_: int
  name: str
  mana: int

class ElderberryEval(FructoseEval):
    
    @staticmethod
    def eval_get_avg_len(yeet, debug):
        @yeet(debug=debug)
        def get_avg_len(words: list[str]) -> int:
          """
          Calculate the average length of the words in a given list.
          """

        get_avg_len(["dog","window","skyscraper"])


    @staticmethod
    def eval_get_theme(yeet, debug):
        @yeet(debug=debug)
        def get_theme(words: list[str]) -> str:
          """
          Figure out a single common theme for the given list of words.
          """

        get_theme(["dog","window","purple"])

    @staticmethod
    def eval_choose_word(yeet, debug):
        @yeet(flavors=["random"], debug=debug)
        def choose_word() -> str:
          """
          Choose a random word for the user to guess in a hangman game. The list of words can be anything, however varied. And obscure words are preferred. The categories can be anything and mixed.
          """

        choose_word()

    @staticmethod
    def eval_choose_words(yeet, debug):
        @yeet(flavors=["random"], debug=debug)
        def choose_words(n: int) -> list[str]:
          """
          Choose n random words for the user to guess in a hangman game. The list of words can be anything, however varied. Prefers obscure words. The categories can be anything and mixed.
          """

        choose_words(2)

    @staticmethod
    def eval_guess_letter(yeet, debug):
        @yeet(debug=debug)
        def guess_letter(word: str, letter: str) -> bool:
          """
          Check if the letter is in the word.
          """

        guess_letter("xertz", "t")

    @staticmethod
    def eval_generate_data(yeet, debug):
        @yeet(debug=debug)
        def generate_data(schema: str) -> dict:
          """
          Generate data based on the given schema.
          """

        generate_data("name:str,age:int,city:str")

    @staticmethod
    def eval_generate_dataclass(yeet, debug):
        @yeet(debug=debug)
        def generate_dataclass() -> House:
          """
          Generate data based on the given schema.
          """

        generate_dataclass()

    # TODO: more interesting eval based on content
    @staticmethod
    def eval_draw_ascii_art(yeet, debug):
        @yeet(flavors=["random"], debug=debug)
        def draw_ascii_art() -> str:
          """
          Give me a copy-pasteable example of a random complex multi-line ASCII art.
          """

        draw_ascii_art()
        
    # TODO: more interesting eval based on content
    @staticmethod
    def eval_receive_attack(yeet, debug):
        @yeet(flavors=["random"], debug=debug)
        def receive_attack(player_state: Player, dmg: int, crit_chance: float) -> Player:
          """
          Simulate a player receiving an attack. If crit, then double the dmg amount. Crit is randomly rolled during this turn based on crit_chance. Subtracts def_ from final dmg.
          """

        receive_attack({"hp": 100, "def_": 10, "name": "Jack Sparrow", "mana": 55}, 12, 0.3)
        
    # TODO: starts with <a and contains "https://github.com/bananaml/fructose"
    @staticmethod
    def eval_write_github_stars_badge_html(yeet, debug):
        @yeet(debug=debug)
        def write_github_stars_badge_html(repo: str) -> str:
          """
          Write HTML to display a GitHub stars badge for a given repo.
          """

        write_github_stars_badge_html("bananaml/fructose")
