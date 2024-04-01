from fructose import Fructose
ai = Fructose()

@ai
def describe(animals: list[str]) -> str:
  """
  Given a list of animals, use one word that'd describe them all.
  """
  ...

description = describe(["dog", "cat", "parrot", "goldfish"])
print(description) # -> "pets" type: str