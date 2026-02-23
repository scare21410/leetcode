#!/usr/bin/env python3
"""Test runner for Go solutions. Generates solution_test.go files, runs go test, cleans up."""

import json
import os
import shutil
import subprocess
import sys
import tempfile

PROBLEMS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'problems')
ROOT_DIR = os.path.join(os.path.dirname(__file__), '..', '..')


def camel_to_pascal(name):
    return name[0].upper() + name[1:]


def go_type_of(value):
    if isinstance(value, bool):
        return 'bool'
    elif isinstance(value, int):
        return 'int'
    elif isinstance(value, float):
        return 'float64'
    elif isinstance(value, str):
        return 'string'
    elif isinstance(value, list):
        if not value:
            return '[]int'
        return '[]' + go_type_of(value[0])
    return 'interface{}'


def json_to_go(value):
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
            return 'nil'
        t = go_type_of(value)
        inner = ', '.join(json_to_go(v) for v in value)
        return f'{t}{{{inner}}}'
    elif value is None:
        return 'nil'
    raise ValueError(f"Unsupported type: {type(value)}")


def has_listnode(testcases):
    param_types = testcases.get('paramTypes', [])
    return_type = testcases.get('returnType', '')
    return 'ListNode' in param_types or return_type == 'ListNode'


def generate_test(testcases):
    func_name = testcases['function']
    test_name = camel_to_pascal(func_name)
    param_types = testcases.get('paramTypes', [])
    return_type = testcases.get('returnType', '')
    uses_listnode = has_listnode(testcases)

    lines = [
        'package solution',
        '',
        'import (',
        '\t"reflect"',
        '\t"testing"',
        ')',
        '',
    ]

    if uses_listnode:
        lines.extend([
            'type ListNode struct {',
            '\tVal  int',
            '\tNext *ListNode',
            '}',
            '',
            'func arrayToListNode(arr []int) *ListNode {',
            '\tdummy := &ListNode{}',
            '\tcur := dummy',
            '\tfor _, v := range arr {',
            '\t\tcur.Next = &ListNode{Val: v}',
            '\t\tcur = cur.Next',
            '\t}',
            '\treturn dummy.Next',
            '}',
            '',
            'func listNodeToArray(node *ListNode) []int {',
            '\tarr := []int{}',
            '\tfor node != nil {',
            '\t\tarr = append(arr, node.Val)',
            '\t\tnode = node.Next',
            '\t}',
            '\treturn arr',
            '}',
            '',
        ])

    lines.append(f'func Test{test_name}(t *testing.T) {{')

    for i, case in enumerate(testcases['cases']):
        lines.append(f'\tt.Run("case_{i}", func(t *testing.T) {{')
        args = []
        for j, arg in enumerate(case['input']):
            ptype = param_types[j] if j < len(param_types) else ''
            if ptype == 'ListNode':
                lines.append(f'\t\tarr{j} := {json_to_go(arg)}')
                lines.append(f'\t\targ{j} := arrayToListNode(arr{j})')
            else:
                lines.append(f'\t\targ{j} := {json_to_go(arg)}')
            args.append(f'arg{j}')

        if return_type == 'ListNode':
            lines.append(f'\t\texpected := {json_to_go(case["output"])}')
            lines.append(f'\t\tresultNode := {func_name}({", ".join(args)})')
            lines.append('\t\tresult := listNodeToArray(resultNode)')
        else:
            lines.append(f'\t\texpected := {json_to_go(case["output"])}')
            lines.append(f'\t\tresult := {func_name}({", ".join(args)})')

        lines.append('\t\tif !reflect.DeepEqual(result, expected) {')
        lines.append('\t\t\tt.Errorf("got %v, want %v", result, expected)')
        lines.append('\t\t}')
        lines.append('\t})')

    lines.append('}')
    lines.append('')
    return '\n'.join(lines)


def main():
    generated = []
    found = False

    for entry in sorted(os.listdir(PROBLEMS_DIR)):
        problem_dir = os.path.join(PROBLEMS_DIR, entry)
        solution = os.path.join(problem_dir, 'solution.go')
        testcases_file = os.path.join(problem_dir, 'testcases.json')

        if not (os.path.isfile(solution) and os.path.isfile(testcases_file)):
            continue

        found = True
        with open(testcases_file) as f:
            testcases = json.load(f)

        test_content = generate_test(testcases)
        test_path = os.path.join(problem_dir, 'solution_test.go')
        with open(test_path, 'w') as f:
            f.write(test_content)
        generated.append((problem_dir, test_path))

    if not found:
        print("No Go solutions found.")
        return 0

    all_passed = True
    try:
        for problem_dir, test_path in generated:
            with tempfile.TemporaryDirectory() as tmpdir:
                with open(os.path.join(problem_dir, 'solution.go')) as src:
                    content = src.read()
                with open(os.path.join(tmpdir, 'solution.go'), 'w') as dst:
                    dst.write('package solution\n\n' + content)
                shutil.copy(test_path, tmpdir)
                shutil.copy(os.path.join(ROOT_DIR, 'go.mod'), tmpdir)
                for extra in ['go.sum', '.tool-versions']:
                    p = os.path.join(ROOT_DIR, extra)
                    if os.path.exists(p):
                        shutil.copy(p, tmpdir)
                result = subprocess.run(
                    ['go', 'test', '-v', '.'],
                    cwd=tmpdir,
                )
                if result.returncode != 0:
                    all_passed = False
    finally:
        for _, test_path in generated:
            if os.path.exists(test_path):
                os.unlink(test_path)

    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
