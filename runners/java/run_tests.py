#!/usr/bin/env python3
"""Test runner for Java solutions. Generates test class, compiles, runs, cleans up."""

import json
import os
import subprocess
import sys

PROBLEMS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'problems')


def json_to_java(value):
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
            return 'new int[]{}'
        if isinstance(value[0], int):
            inner = ', '.join(str(v) for v in value)
            return f'new int[]{{{inner}}}'
        elif isinstance(value[0], str):
            inner = ', '.join(f'"{v}"' for v in value)
            return f'new String[]{{{inner}}}'
        elif isinstance(value[0], list):
            inner = ', '.join(json_to_java(v) for v in value)
            return f'new int[][]{{{inner}}}'
    elif value is None:
        return 'null'
    raise ValueError(f"Unsupported type: {type(value)}")


def has_listnode(testcases):
    param_types = testcases.get('paramTypes', [])
    return_type = testcases.get('returnType', '')
    return 'ListNode' in param_types or return_type == 'ListNode'


def generate_test(testcases):
    func = testcases['function']
    param_types = testcases.get('paramTypes', [])
    return_type = testcases.get('returnType', '')
    uses_listnode = has_listnode(testcases)

    lines = [
        'import java.util.Arrays;',
        'import java.util.ArrayList;',
        '',
    ]

    if uses_listnode:
        lines.extend([
            'class ListNode {',
            '    int val;',
            '    ListNode next;',
            '    ListNode() {}',
            '    ListNode(int val) { this.val = val; }',
            '    ListNode(int val, ListNode next) { this.val = val; this.next = next; }',
            '}',
            '',
        ])

    lines.extend([
        'public class TestSolution {',
    ])

    if uses_listnode:
        lines.extend([
            '    static ListNode arrayToListNode(int[] arr) {',
            '        ListNode dummy = new ListNode();',
            '        ListNode cur = dummy;',
            '        for (int v : arr) {',
            '            cur.next = new ListNode(v);',
            '            cur = cur.next;',
            '        }',
            '        return dummy.next;',
            '    }',
            '',
            '    static int[] listNodeToArray(ListNode node) {',
            '        ArrayList<Integer> list = new ArrayList<>();',
            '        while (node != null) {',
            '            list.add(node.val);',
            '            node = node.next;',
            '        }',
            '        return list.stream().mapToInt(Integer::intValue).toArray();',
            '    }',
            '',
        ])

    lines.extend([
        '    public static void main(String[] args) {',
        '        Solution sol = new Solution();',
        '        int passed = 0, failed = 0;',
    ])

    for i, case in enumerate(testcases['cases']):
        lines.append('        {')

        # Build arguments
        arg_parts = []
        for j, arg in enumerate(case['input']):
            ptype = param_types[j] if j < len(param_types) else ''
            if ptype == 'ListNode':
                lines.append(f'            int[] arr{j} = {json_to_java(arg)};')
                lines.append(f'            ListNode arg{j} = arrayToListNode(arr{j});')
                arg_parts.append(f'arg{j}')
            else:
                arg_parts.append(json_to_java(arg))

        call_args = ', '.join(arg_parts)

        if return_type == 'ListNode':
            lines.append(f'            ListNode resultNode = sol.{func}({call_args});')
            lines.append('            int[] result = listNodeToArray(resultNode);')
            expected = json_to_java(case['output'])
            lines.append(f'            int[] expected = {expected};')
            lines.append('            if (Arrays.equals(result, expected)) {')
            lines.append('                passed++;')
            lines.append('            } else {')
            lines.append('                failed++;')
            lines.append(f'                System.out.println("FAIL case {i}: got " + Arrays.toString(result) + ", want " + Arrays.toString(expected));')
            lines.append('            }')
        else:
            expected = json_to_java(case['output'])
            is_array = isinstance(case['output'], list)
            lines.append(f'            var result = sol.{func}({call_args});')
            lines.append(f'            var expected = {expected};')
            if is_array:
                lines.append('            if (Arrays.equals(result, expected)) {')
            else:
                lines.append('            if (result == expected) {')
            lines.append('                passed++;')
            lines.append('            } else {')
            lines.append('                failed++;')
            if is_array:
                lines.append(f'                System.out.println("FAIL case {i}: got " + Arrays.toString(result) + ", want " + Arrays.toString(expected));')
            else:
                lines.append(f'                System.out.println("FAIL case {i}: got " + result + ", want " + expected);')
            lines.append('            }')

        lines.append('        }')

    lines.extend([
        '        System.out.println(passed + " passed, " + failed + " failed");',
        '        if (failed > 0) System.exit(1);',
        '    }',
        '}',
    ])
    return '\n'.join(lines)


def main():
    all_passed = True
    found = False

    for entry in sorted(os.listdir(PROBLEMS_DIR)):
        problem_dir = os.path.join(PROBLEMS_DIR, entry)
        solution = os.path.join(problem_dir, 'Solution.java')
        testcases_file = os.path.join(problem_dir, 'testcases.json')

        if not (os.path.isfile(solution) and os.path.isfile(testcases_file)):
            continue

        found = True
        print(f"\n=== {entry} ===")

        with open(testcases_file) as f:
            testcases = json.load(f)

        test_content = generate_test(testcases)
        test_file = os.path.join(problem_dir, 'TestSolution.java')

        with open(test_file, 'w') as f:
            f.write(test_content)

        cleanup_files = ['TestSolution.java', 'Solution.class', 'TestSolution.class']
        if has_listnode(testcases):
            cleanup_files.append('ListNode.class')

        try:
            compile_result = subprocess.run(
                ['javac', 'Solution.java', 'TestSolution.java'],
                cwd=problem_dir, capture_output=True, text=True,
            )
            if compile_result.returncode != 0:
                print(f"COMPILE ERROR:\n{compile_result.stderr}")
                all_passed = False
                continue

            run_result = subprocess.run(
                ['java', 'TestSolution'],
                cwd=problem_dir, capture_output=True, text=True,
            )
            print(run_result.stdout.strip())
            if run_result.returncode != 0:
                all_passed = False
        finally:
            for name in cleanup_files:
                p = os.path.join(problem_dir, name)
                if os.path.exists(p):
                    os.unlink(p)

    if not found:
        print("No Java solutions found.")
        return 0

    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
