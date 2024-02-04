from fructose import AI

@AI(debug=True)
def get_theme(words: list[str]) -> str:
  """
  This function takes a list of words and returns a theme.
  """

theme = get_theme(["cat", "dog", "bird"])


print("---- Evaluating the result ----")

print("Theme:\t\t", theme)
# assert theme == "animals" # not deterministic

print("Type:\t\t", type(theme))
assert type(theme) == str

