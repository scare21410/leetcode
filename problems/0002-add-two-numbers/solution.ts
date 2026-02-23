class ListNode {
    val: number
    next: ListNode | null
    constructor(val?: number, next?: ListNode | null) {
        this.val = (val===undefined ? 0 : val)
         this.next = (next===undefined ? null : next)
    }
}

function addDigits(l1: ListNode | null, l2: ListNode | null, carry: 0 | 1): ListNode {
    if (!l1 && !l2) {
        throw new Error('Invalid state, both digit nodes are null');
    }
    const value = carry + (l1?.val ?? 0) + (l2?.val ?? 0);
    const digitCarry = value > 9 ? 1 : 0;
    const digitValue = value % 10;
    if (!l1?.next && !l2?.next) {
        const carryNode = digitCarry ? new ListNode(digitCarry) : null;
        return new ListNode(digitValue, carryNode);
    }
    return new ListNode(digitValue, addDigits(l1?.next ?? null, l2?.next ?? null, digitCarry));
}

export function addTwoNumbers(l1: ListNode | null, l2: ListNode | null): ListNode | null {
    if (!l1 && !l2) {
        return null;
    }
    if (!l1) {
        return l2;
    }
    if (!l2) {
        return l1;
    }


    return addDigits(l1, l2, 0);
};