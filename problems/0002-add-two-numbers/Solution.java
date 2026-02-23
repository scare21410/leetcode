/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    private ListNode addDigits(ListNode l1, ListNode l2, int carry) {
        if (l1 == null && l2 == null) {
            throw new RuntimeException("Invalid state, both lists are null");
        }
        int value = carry + (l1 == null ? 0 : l1.val) + (l2 == null ? 0 : l2.val);
        int digitCarry = value / 10;
        int digitValue = value % 10;
        boolean hasNextL1 = l1 != null && l1.next != null;
        boolean hasNextL2 = l2 != null && l2.next != null;
        if (!hasNextL1 && !hasNextL2) {
            ListNode carryNode = digitCarry > 0 ? new ListNode(digitCarry) : null;
            return new ListNode(digitValue, carryNode);
        }
        return new ListNode(
            digitValue,
            addDigits(
                l1 != null ? l1.next : null,
                l2 != null ? l2.next : null,
                digitCarry
            )
        );
    }

    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        if (l1 == null && l2 == null) {
            return null;
        }
        if (l1 == null) {
            return l2;
        }
        if (l2 == null) {
            return l1;
        }

        return this.addDigits(l1, l2, 0);
    }
}