import sys
sys.path.append('/Users/nik/dev/banana/fructose/src')

# print(sys.path)


from fructose import AI




@AI(debug=True)
def get_avg_len(words: list[str]) -> int:
  """
  Calculate the average length of the words in a given list.
  """

theme = get_avg_len(["cats", "antelopes"])

print(theme) # 3
print(type(theme)) # <class 'int'>


