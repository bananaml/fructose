from fructose import Fructose

human = Fructose()

@human()
def repeat(input_str: str) -> str:
    """
    repeat back the input_str
    """
    ...

print(repeat("Ahoy"))



