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
  paramTypes?: string[];
  returnType?: string;
  cases: TestCase[];
}

class ListNode {
  val: number;
  next: ListNode | null;
  constructor(val: number = 0, next: ListNode | null = null) {
    this.val = val;
    this.next = next;
  }
}

function arrayToListNode(arr: number[]): ListNode | null {
  const dummy = new ListNode();
  let cur = dummy;
  for (const v of arr) {
    cur.next = new ListNode(v);
    cur = cur.next;
  }
  return dummy.next;
}

function listNodeToArray(node: ListNode | null): number[] {
  const arr: number[] = [];
  while (node) {
    arr.push(node.val);
    node = node.next;
  }
  return arr;
}

function discoverProblems() {
  const entries = fs.readdirSync(PROBLEMS_DIR).sort();
  const problems: Array<{ name: string; dir: string; testcases: TestCases }> = [];

  const problemFilter = process.env.PROBLEM || '';
  for (const entry of entries) {
    if (problemFilter && !entry.includes(problemFilter)) continue;
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

        const paramTypes = problem.testcases.paramTypes || [];
        const returnType = problem.testcases.returnType || '';

        // Inject ListNode into module if needed
        if (mod.ListNode === undefined && paramTypes.includes('ListNode')) {
          // solution may define its own ListNode; if not, we use ours
        }

        const args = tc.input.map((arg, j) => {
          if (paramTypes[j] === 'ListNode') {
            return arrayToListNode(arg as number[]);
          }
          return arg;
        });

        let result = fn(...args);

        if (returnType === 'ListNode') {
          result = listNodeToArray(result);
        }

        expect(result).toEqual(tc.output);
      });
    }
  });
}
