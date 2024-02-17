from dataclasses import dataclass
import sys
from concurrent.futures import ThreadPoolExecutor
import time

from pydantic_core.core_schema import time_schema
from fructose import Fructose

ai = Fructose()

thread_pool = ThreadPoolExecutor(max_workers=100)

DEBUG = True

@dataclass
class EvalResult:
    execution_time: float
    score: int

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

        total_execution_time = 0
        num_execuations = 0

        futures = []
        for func in functions:
            print(f"running {func}")

            def run(func):
                start_time = time.time()
                result = 1
                try:
                    getattr(cls, func)(ai, DEBUG)
                    print(f"\033[92m{func} passed\033[0m")
                except Exception as e:
                    print(f"\033[91m{func} failed\033[0m")
                    print(e)
                    result = 0

                execution_time = time.time() - start_time

                return EvalResult(execution_time, result)

            futures.append(thread_pool.submit(run, func))

        for future in futures:
            result = future.result()
            score += result.score
            total_execution_time += result.execution_time
            num_execuations += 1

        avg_execution_time = total_execution_time / num_execuations

        print("\n\n#########\nEvaluation complete\n#########")
        print(f"Score: {score}/{len(functions)}")
        print(f"Average execution time: {avg_execution_time} seconds")
        print(f"Percentage: {score/len(functions) * 100}%")

