from enum import Enum
from core import FructoseEval
from dataclasses import dataclass

@dataclass
class House:
  color: str
  size: int
  is_occupied: bool 

@dataclass
class Person:
  name: str
  age: int
  city: str
  home: House


@dataclass
class Player:
  hp: int
  def_: int
  name: str
  mana: int

class Color(Enum):
    LAVENDER = "lavender"
    INDIGO = "indigo"
    TERRACOTTA = "terracotta"


class ElderberryEval(FructoseEval):
    """
    Most of these are trivial and not a reflection of how fructose should actually be used.

    They're mostly for testing purposes, especially type-checking.
    """
    
    @staticmethod
    def eval_get_avg_len(ai, debug):
        @ai(debug=debug)
        def get_avg_len(words: list[str]) -> int:
          """
          Calculate the average length of the words in a given list.
          """

        get_avg_len(["dog","window","skyscraper"])


    @staticmethod
    def eval_get_theme(ai, debug):
        @ai(debug=debug)
        def get_theme(words: list[str]) -> str:
          """
          Figure out a single common theme for the given list of words.
          """

        get_theme(["dog","window","purple"])

    @staticmethod
    def eval_choose_word(ai, debug):
        @ai(flavors=["random"], debug=debug)
        def choose_word() -> str:
          """
          Choose a random word for the user to guess in a hangman game. The list of words can be anything, however varied. And obscure words are preferred. The categories can be anything and mixed.
          """

        choose_word()

    @staticmethod
    def eval_choose_words(ai, debug):
        @ai(flavors=["random"], debug=debug)
        def choose_words(n: int) -> list[str]:
          """
          Choose n random words for the user to guess in a hangman game. The list of words can be anything, however varied. Prefers obscure words. The categories can be anything and mixed.
          """

        choose_words(2)

    @staticmethod
    def eval_guess_letter(ai, debug):
        @ai(debug=debug)
        def guess_letter(word: str, letter: str) -> bool:
          """
          Check if the letter is in the word.
          """

        guess_letter("xertz", "t")

    @staticmethod
    def eval_generate_data(ai, debug):
        @ai(debug=debug)
        def generate_data(schema: str) -> dict[str, str]:
          """
          Generate data based on the given schema.
          """

        generate_data("name:str,age:int,city:str")

    @staticmethod
    def eval_generate_dataclass(ai, debug):
        @ai(debug=debug)
        def generate_dataclass() -> House:
          """
          Generate data based on the given schema.
          """

        generate_dataclass()

    @staticmethod
    def eval_nested_dataclass(ai, debug):
        @ai(debug=debug)
        def nested_dataclass() -> Person:
          """
          Generate data based on the given schema.
          """

        nested_dataclass()

    @staticmethod
    def eval_enum(ai, debug):
        @ai(debug=debug)
        def enum() -> Color:
          """
          Pick a random color
          """

        enum()

    # TODO: more interesting eval based on content
    @staticmethod
    def eval_draw_ascii_art(ai, debug):
        @ai(flavors=["random"], debug=debug)
        def draw_ascii_art() -> str:
          """
          Give me a copy-pasteable example of a random complex multi-line ASCII art.
          """

        draw_ascii_art()
        
    # TODO: more interesting eval based on content
    @staticmethod
    def eval_receive_attack(ai, debug):
        @ai(flavors=["random"], debug=debug)
        def receive_attack(player_state: Player, dmg: int, crit_chance: float) -> Player:
          """
          Simulate a player receiving an attack. If crit, then double the dmg amount. Crit is randomly rolled during this turn based on crit_chance. Subtracts def_ from final dmg.
          """

        receive_attack({"hp": 100, "def_": 10, "name": "Jack Sparrow", "mana": 55}, 12, 0.3)
        
    # TODO: starts with <a and contains "https://github.com/bananaml/fructose"
    @staticmethod
    def eval_write_github_stars_badge_html(ai, debug):
        @ai(debug=debug)
        def write_github_stars_badge_html(repo: str) -> str:
          """
          Write HTML to display a GitHub stars badge for a given repo.
          """

        write_github_stars_badge_html("bananaml/fructose")

    @staticmethod
    def eval_deep_nesting_out(ai, debug):
        @ai(debug=debug)

        def deep_nesting() -> dict[str, dict[str, list[dict[str, list[str]]]]]:
          """
          Generate a deeply nested data structure.
          """
        deep_nesting()

    @staticmethod
    def eval_deep_nesting_in(ai, debug):
        @ai(debug=debug)

        def deep_nesting(input: dict[str, dict[str, list[dict[str, list[str]]]]]) -> str:
          """
          Stringify the deeply nested data structure.
          """
        deep_nesting({"a": {"b": [{"c": ["d", "e"]}, {"f": ["g", "h", "i"]}]} })