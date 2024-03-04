from fructose import Fructose
import random

ai = Fructose()

def add(a: float, b: float) -> float:
    """
    Adds two floats
    """
    return a + b

def multiply(a: float, b: float) -> float:
    """
    Multiplies two floats
    """
    return a * b

@ai(
    uses=[
        add,
        multiply
    ],
    debug=True
)
def ask(question: str) -> str:
    """
    Answer the user's questions as best as you can
    """

print(ask("Jessica is planning to buy notebooks for the new school year. If each notebook costs $3 and she has a $10 coupon from the store, how many notebooks can she buy if she has $30 to spend?"))
