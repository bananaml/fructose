import sys
sys.path.append('/Users/nik/dev/banana/fructose/src')

from typing import Dict, List, Set, Tuple
# print(sys.path)


from fructose import send




@send(debug=True)
def get_avg_len(words: list[str]) -> int:
  """
  Calculate the average length of the words in a given list.
  """

@send(debug=True)
def get_theme(words: list[str]) -> str:
  """
  Figure out a single common theme for the given list of words.
  """

# length = get_avg_len(["dog","window","skyscraper"])
# theme = get_theme(["dog","window","purple"])


##### HANGMAN

@send(debug=True)
def choose_word() -> str:
  """
  Choose a random word for the user to guess in a hangman game. The list of words can be anything, however varied. Prefer obscure words. The categories can be anything and mixed.
  """

@send(debug=True)
def choose_words(n: int) -> list[str]:
  """
  Choose n random words for the user to guess in a hangman game. The list of words can be anything, however varied. Prefer obscure words. The categories can be anything and mixed.
  """

@send(debug=True)
def guess_letter(word: str, letter: str) -> bool:
  """
  Check if the letter is in the word.
  """

# word = choose_word()
word = choose_words(2)

# guess = guess_letter("xertz", "t")

#####



##### SCHEMA

@send(debug=True)
def generate_data(schema: str) -> dict:
  """
  Generate 5 rows of sample data based on the given schema. Make the names funny.
  """


# data = generate_data("id:int, name:str, age:int, email:str, phone:str")

#####

# theme = get_theme(["cats", "antelopes"])
# print(theme) # 3
# print(type(theme)) # <class 'int'>








# fructose create

# "I want to create a hangman-type game"







