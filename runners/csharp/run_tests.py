#!/usr/bin/env python3
"""Test runner for C# solutions. Creates temp dotnet project, compiles, runs, cleans up."""

import json
import os
import re
import subprocess
import sys
import tempfile
import shutil

PROBLEMS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'problems')


def detect_dotnet_tfm():
    try:
        result = subprocess.run(['dotnet', '--version'], capture_output=True, text=True)
        major = int(result.stdout.strip().split('.')[0])
        return f'net{major}.0'
    except Exception:
        return 'net8.0'


def camel_to_pascal(name):
    return name[0].upper() + name[1:]


def json_to_csharp(value):
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
            return 'Array.Empty<int>()'
        if isinstance(value[0], int):
            inner = ', '.join(str(v) for v in value)
            return f'new int[] {{{inner}}}'
        elif isinstance(value[0], str):
            inner = ', '.join(f'"{v}"' for v in value)
            return f'new string[] {{{inner}}}'
        elif isinstance(value[0], list):
            inner = ', '.join(json_to_csharp(v) for v in value)
            return f'new int[][] {{{inner}}}'
    elif value is None:
        return 'null'
    raise ValueError(f"Unsupported type: {type(value)}")


def generate_test(testcases):
    func = camel_to_pascal(testcases['function'])
    lines = [
        'using System;',
        'using System.Linq;',
        '',
        'public class TestSolution {',
        '    public static void Main() {',
        '        var sol = new Solution();',
        '        int passed = 0, failed = 0;',
    ]

    for i, case in enumerate(testcases['cases']):
        args = ', '.join(json_to_csharp(a) for a in case['input'])
        expected = json_to_csharp(case['output'])
        is_array = isinstance(case['output'], list)

        lines.append('        {')
        lines.append(f'            var result = sol.{func}({args});')
        lines.append(f'            var expected = {expected};')
        if is_array:
            lines.append('            if (result.SequenceEqual(expected)) {')
        else:
            lines.append('            if (result == expected) {')
        lines.append('                passed++;')
        lines.append('            } else {')
        lines.append('                failed++;')
        if is_array:
            lines.append(f'                var got = "[" + string.Join(", ", result) + "]";')
            lines.append(f'                var want = "[" + string.Join(", ", expected) + "]";')
            lines.append(f'                Console.WriteLine("FAIL case {i}: got " + got + ", want " + want);')
        else:
            lines.append(f'                Console.WriteLine("FAIL case {i}: got " + result + ", want " + expected);')
        lines.append('            }')
        lines.append('        }')

    lines.extend([
        '        Console.WriteLine(passed + " passed, " + failed + " failed");',
        '        if (failed > 0) Environment.Exit(1);',
        '    }',
        '}',
    ])
    return '\n'.join(lines)


def main():
    all_passed = True
    found = False

    for entry in sorted(os.listdir(PROBLEMS_DIR)):
        problem_dir = os.path.join(PROBLEMS_DIR, entry)
        solution = os.path.join(problem_dir, 'Solution.cs')
        testcases_file = os.path.join(problem_dir, 'testcases.json')

        if not (os.path.isfile(solution) and os.path.isfile(testcases_file)):
            continue

        found = True
        print(f"\n=== {entry} ===")

        with open(testcases_file) as f:
            testcases = json.load(f)

        test_content = generate_test(testcases)

        with tempfile.TemporaryDirectory() as tmpdir:
            tfm = detect_dotnet_tfm()
            with open(os.path.join(tmpdir, 'Test.csproj'), 'w') as f:
                f.write('<Project Sdk="Microsoft.NET.Sdk">\n')
                f.write('  <PropertyGroup>\n')
                f.write('    <OutputType>Exe</OutputType>\n')
                f.write(f'    <TargetFramework>{tfm}</TargetFramework>\n')
                f.write('  </PropertyGroup>\n')
                f.write('</Project>\n')

            shutil.copy(solution, os.path.join(tmpdir, 'Solution.cs'))

            with open(os.path.join(tmpdir, 'Program.cs'), 'w') as f:
                f.write(test_content)

            run_result = subprocess.run(
                ['dotnet', 'run', '--project', tmpdir],
                capture_output=True, text=True,
            )
            print(run_result.stdout.strip())
            if run_result.stderr.strip():
                for line in run_result.stderr.strip().split('\n'):
                    if 'error' in line.lower():
                        print(line)
            if run_result.returncode != 0:
                all_passed = False

    if not found:
        print("No C# solutions found.")
        return 0

    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
