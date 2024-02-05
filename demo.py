from fructose import AI

@AI(debug=True)
def get_avg_len(words: list[str]) -> int:
  """
  Input is a list of words, output is the average length of the words.
  """

theme = get_avg_len(["cat", "dog"])

print(theme) # 3
print(type(theme)) # <class 'int'>

get_avg_len = ai({"words": list[str]}, int)
