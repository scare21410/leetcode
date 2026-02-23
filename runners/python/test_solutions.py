import json
import importlib.util
import os

import pytest

PROBLEMS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'problems')


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __eq__(self, other):
        a, b = self, other
        while a and b:
            if a.val != b.val:
                return False
            a, b = a.next, b.next
        return a is None and b is None


def array_to_listnode(arr):
    dummy = ListNode()
    cur = dummy
    for v in arr:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def listnode_to_array(node):
    arr = []
    while node:
        arr.append(node.val)
        node = node.next
    return arr


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
            param_types = data.get('paramTypes', [])
            return_type = data.get('returnType', '')
            for i, case in enumerate(data['cases']):
                problems.append(
                    pytest.param(
                        solution_file,
                        func_name,
                        case['input'],
                        case['output'],
                        param_types,
                        return_type,
                        id=f"{entry}/case_{i}",
                    )
                )
    return problems


@pytest.mark.parametrize(
    "solution_file,func_name,input_args,expected,param_types,return_type",
    discover(),
)
def test_solution(solution_file, func_name, input_args, expected, param_types, return_type):
    spec = importlib.util.spec_from_file_location("solution", solution_file)
    module = importlib.util.module_from_spec(spec)
    module.ListNode = ListNode
    spec.loader.exec_module(module)
    sol = module.Solution()
    func = getattr(sol, func_name)

    converted_args = []
    for j, arg in enumerate(input_args):
        ptype = param_types[j] if j < len(param_types) else ''
        if ptype == 'ListNode':
            converted_args.append(array_to_listnode(arg))
        else:
            converted_args.append(arg)

    result = func(*converted_args)

    if return_type == 'ListNode':
        result = listnode_to_array(result)

    assert result == expected
