from fructose import AI

@AI(debug=True)
def get_avg_len(words: list[str]) -> dict[str, int]:
  """
  Input is a list of words, output is the average length of the words.
  """

theme = get_avg_len(["cat", "dog"])

print(theme) # 4
print(type(theme)) # <class 'int'>


