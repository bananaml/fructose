# This examples demonstrates how to use Fructose to simulate an RPG "turn" where a player is attacked.

from fructose import Fructose
from dataclasses import dataclass

# Create a new instance of the Fructose app
ai = Fructose()

# Define a dataclass to represent a player
@dataclass
class Player:
  hp: int
  def_: int
  name: str
  mana: int

# decorate your function to call an LLM. Your ways to guide the LLM are through the docstring,
# functions parameters & arguments and the return type.
# If your function requires explicit randomness, you can specify the uses parameter.
@ai(flavors=["random"], debug=True)
def receive_attack(player_state: Player, dmg: int, crit_chance: float) -> Player:
  """
  Simulates a player receiving an attack. If crit, then double the dmg amount. Crit is randomly rolled during this turn based on crit_chance. Subtracts def_ from final dmg.
  """

def main():
    state = receive_attack({"hp": 100, "def_": 10, "name": "Jack Sparrow", "mana": 55}, 12, 0.3)
    print(state)

if __name__ == "__main__":
    main()


