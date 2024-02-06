from fructose import Fructose

ai = Fructose()

@ai(debug=True)
def get_avg_len(words: list[str]) -> list[str]:
  """
  Calculate the average length of the words in a given list, and repeat that five times.
  """

length = get_avg_len(["dog","window","skyscraper"])
print(length)