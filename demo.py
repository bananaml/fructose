from fructose import Fructose

ai = Fructose()

@ai(debug=True)
def get_avg_len(words: list[str]) -> int:
  """
  Calculate the average length of the words in a given list.
  """

length = get_avg_len(["dog","window","skyscraper"])
print(length)