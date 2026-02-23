#!/usr/bin/env python3
"""Test runner for C++ solutions. Generates test main, compiles, runs, cleans up."""

import json
import os
import subprocess
import sys
import tempfile

PROBLEMS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'problems')


def cpp_type_of(value):
    if isinstance(value, bool):
        return 'bool'
    elif isinstance(value, int):
        return 'int'
    elif isinstance(value, float):
        return 'double'
    elif isinstance(value, str):
        return 'string'
    elif isinstance(value, list):
        if not value:
            return 'vector<int>'
        return f'vector<{cpp_type_of(value[0])}>'
    return 'auto'


def json_to_cpp(value):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    elif isinstance(value, int):
        return str(value)
    elif isinstance(value, float):
        return str(value)
    elif isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, list):
        if not value:
            return '{}'
        inner = ', '.join(json_to_cpp(v) for v in value)
        return '{' + inner + '}'
    elif value is None:
        return 'nullptr'
    raise ValueError(f"Unsupported type: {type(value)}")


def has_listnode(testcases):
    param_types = testcases.get('paramTypes', [])
    return_type = testcases.get('returnType', '')
    return 'ListNode' in param_types or return_type == 'ListNode'


def generate_test(testcases, solution_filename):
    func = testcases['function']
    param_types = testcases.get('paramTypes', [])
    return_type = testcases.get('returnType', '')
    uses_listnode = has_listnode(testcases)

    lines = [
        f'#include "{solution_filename}"',
        '#include <iostream>',
        '#include <cassert>',
        '#include <vector>',
        '',
        'using namespace std;',
        '',
    ]

    if uses_listnode:
        lines.extend([
            'ListNode* arrayToListNode(const vector<int>& arr) {',
            '    ListNode dummy(0);',
            '    ListNode* cur = &dummy;',
            '    for (int v : arr) {',
            '        cur->next = new ListNode(v);',
            '        cur = cur->next;',
            '    }',
            '    return dummy.next;',
            '}',
            '',
            'vector<int> listNodeToArray(ListNode* node) {',
            '    vector<int> arr;',
            '    while (node) {',
            '        arr.push_back(node->val);',
            '        node = node->next;',
            '    }',
            '    return arr;',
            '}',
            '',
            'void freeList(ListNode* node) {',
            '    while (node) {',
            '        ListNode* tmp = node;',
            '        node = node->next;',
            '        delete tmp;',
            '    }',
            '}',
            '',
        ])

    lines.extend([
        'template<typename T>',
        'string vec_to_str(const vector<T>& v) {',
        '    string s = "[";',
        '    for (size_t i = 0; i < v.size(); i++) {',
        '        if (i > 0) s += ", ";',
        '        s += to_string(v[i]);',
        '    }',
        '    return s + "]";',
        '}',
        '',
        'int main() {',
        '    Solution sol;',
        '    int passed = 0, failed = 0;',
    ])

    for i, case in enumerate(testcases['cases']):
        lines.append(f'    {{ // case {i}')
        arg_names = []
        for j, arg in enumerate(case['input']):
            ptype = param_types[j] if j < len(param_types) else ''
            if ptype == 'ListNode':
                t = cpp_type_of(arg)
                lit = json_to_cpp(arg)
                lines.append(f'        {t} arr{j} = {lit};')
                lines.append(f'        ListNode* arg{j} = arrayToListNode(arr{j});')
            else:
                t = cpp_type_of(arg)
                lit = json_to_cpp(arg)
                lines.append(f'        {t} arg{j} = {lit};')
            arg_names.append(f'arg{j}')

        if return_type == 'ListNode':
            lines.append(f'        ListNode* resultNode = sol.{func}({", ".join(arg_names)});')
            lines.append(f'        vector<int> result = listNodeToArray(resultNode);')
            expected_t = cpp_type_of(case['output'])
            expected_lit = json_to_cpp(case['output'])
            lines.append(f'        {expected_t} expected = {expected_lit};')
            lines.append('        if (result == expected) {')
            lines.append('            passed++;')
            lines.append('        } else {')
            lines.append('            failed++;')
            lines.append(f'            cout << "FAIL case {i}: got " << vec_to_str(result) << ", want " << vec_to_str(expected) << endl;')
            lines.append('        }')
            lines.append('        freeList(resultNode);')
        else:
            expected_t = cpp_type_of(case['output'])
            expected_lit = json_to_cpp(case['output'])
            lines.append(f'        {expected_t} expected = {expected_lit};')
            lines.append(f'        auto result = sol.{func}({", ".join(arg_names)});')
            lines.append('        if (result == expected) {')
            lines.append('            passed++;')
            lines.append('        } else {')
            lines.append('            failed++;')
            if isinstance(case['output'], list):
                lines.append(f'            cout << "FAIL case {i}: got " << vec_to_str(result) << ", want " << vec_to_str(expected) << endl;')
            else:
                lines.append(f'            cout << "FAIL case {i}: got " << result << ", want " << expected << endl;')
            lines.append('        }')
        lines.append('    }')

    lines.extend([
        '    cout << passed << " passed, " << failed << " failed" << endl;',
        '    return failed > 0 ? 1 : 0;',
        '}',
    ])
    return '\n'.join(lines)


def main():
    all_passed = True
    found = False

    for entry in sorted(os.listdir(PROBLEMS_DIR)):
        problem_dir = os.path.join(PROBLEMS_DIR, entry)
        solution = os.path.join(problem_dir, 'solution.cpp')
        testcases_file = os.path.join(problem_dir, 'testcases.json')

        if not (os.path.isfile(solution) and os.path.isfile(testcases_file)):
            continue

        found = True
        print(f"\n=== {entry} ===")

        with open(testcases_file) as f:
            testcases = json.load(f)

        test_content = generate_test(testcases, 'solution.cpp')
        test_file = os.path.join(problem_dir, 'test_main.cpp')
        binary = os.path.join(problem_dir, 'test_runner')

        with open(test_file, 'w') as f:
            f.write(test_content)

        try:
            compile_result = subprocess.run(
                ['g++', '-std=c++17', '-o', binary, test_file],
                capture_output=True, text=True,
            )
            if compile_result.returncode != 0:
                print(f"COMPILE ERROR:\n{compile_result.stderr}")
                all_passed = False
                continue

            run_result = subprocess.run(
                [binary], capture_output=True, text=True,
            )
            print(run_result.stdout.strip())
            if run_result.returncode != 0:
                all_passed = False
        finally:
            for p in [test_file, binary]:
                if os.path.exists(p):
                    os.unlink(p)

    if not found:
        print("No C++ solutions found.")
        return 0

    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
