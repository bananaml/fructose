import sys
from fructose import Fructose
yeet = Fructose()

DEBUG = True

class FructoseEval():
    def __init_subclass__(cls):
        # list all functions on cls
        functions = [
            attr
            for attr in dir(cls)
            if callable(getattr(cls, attr)) and attr.startswith("eval_")
        ]

        if len(sys.argv) > 1:
            functions = [f for f in functions if f == sys.argv[1]]

        score = 0
        for func in functions:
            print(f"running {func}")

            try:
                getattr(cls, func)(yeet, DEBUG)
                print(f"\033[92m{func} passed\033[0m")
                score += 1
            except Exception as e:
                print(f"\033[91m{func} failed\033[0m")
                print(e)

        print("\n\n#########\nEvaluation complete\n#########")
        print(f"Score: {score}/{len(functions)}")
        print(f"Percentage: {score/len(functions) * 100}%")

