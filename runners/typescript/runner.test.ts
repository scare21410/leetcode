import { describe, it, expect } from 'vitest';
import fs from 'fs';
import path from 'path';

const PROBLEMS_DIR = path.resolve(__dirname, '../../problems');

interface TestCase {
  input: unknown[];
  output: unknown;
}

interface TestCases {
  function: string;
  params: string[];
  cases: TestCase[];
}

function discoverProblems() {
  const entries = fs.readdirSync(PROBLEMS_DIR).sort();
  const problems: Array<{ name: string; dir: string; testcases: TestCases }> = [];

  for (const entry of entries) {
    const dir = path.join(PROBLEMS_DIR, entry);
    const solutionPath = path.join(dir, 'solution.ts');
    const testcasesPath = path.join(dir, 'testcases.json');

    if (fs.existsSync(solutionPath) && fs.existsSync(testcasesPath)) {
      const testcases: TestCases = JSON.parse(fs.readFileSync(testcasesPath, 'utf-8'));
      problems.push({ name: entry, dir, testcases });
    }
  }

  return problems;
}

const problems = discoverProblems();

for (const problem of problems) {
  describe(problem.name, () => {
    for (let i = 0; i < problem.testcases.cases.length; i++) {
      const tc = problem.testcases.cases[i];
      it(`case ${i}: ${JSON.stringify(tc.input)} -> ${JSON.stringify(tc.output)}`, async () => {
        const solutionPath = path.join(problem.dir, 'solution.ts');
        const mod = await import(solutionPath);
        const fn = mod[problem.testcases.function];
        expect(fn).toBeDefined();
        const result = fn(...tc.input);
        expect(result).toEqual(tc.output);
      });
    }
  });
}
