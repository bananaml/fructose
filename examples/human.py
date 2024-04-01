from fructose import Fructose

human = Fructose(human=True)

@human(
    debug=True
)
def repeat(input_str: str) -> str:
    """
    repeat back the input_str
    """
    ...

print(repeat("Ahoy"))



