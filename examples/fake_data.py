# This examples demonstrates how to use Fructose to generate fake data while following a strict schema.

from fructose import Fructose
from dataclasses import dataclass

# Define a dataclass to represent a person
@dataclass
class Person:
    name: str
    age: int
    height: float
    is_human: bool

# Create a new instance of the Fructose
ai = Fructose()

# decorate your function to call an LLM. Your ways to guide the LLM are through the docstring,
# functions parameters & arguments and the return type.
@ai()
def generate_fake_person_data() -> Person:
  """
    Generate fake data for following the schema.
  """


def main():
    persons = generate_fake_person_data()
    print(persons)


if __name__ == "__main__":
    main()


