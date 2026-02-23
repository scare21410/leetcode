import json
import importlib.util
import os

import pytest

PROBLEMS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'problems')


def discover():
    problems = []
    for entry in sorted(os.listdir(PROBLEMS_DIR)):
        problem_dir = os.path.join(PROBLEMS_DIR, entry)
        solution_file = os.path.join(problem_dir, 'solution.py')
        testcases_file = os.path.join(problem_dir, 'testcases.json')
        if os.path.isfile(solution_file) and os.path.isfile(testcases_file):
            with open(testcases_file) as f:
                data = json.load(f)
            func_name = data['function']
            for i, case in enumerate(data['cases']):
                problems.append(
                    pytest.param(
                        solution_file,
                        func_name,
                        case['input'],
                        case['output'],
                        id=f"{entry}/case_{i}",
                    )
                )
    return problems


@pytest.mark.parametrize("solution_file,func_name,input_args,expected", discover())
def test_solution(solution_file, func_name, input_args, expected):
    spec = importlib.util.spec_from_file_location("solution", solution_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sol = module.Solution()
    func = getattr(sol, func_name)
    assert func(*input_args) == expected
