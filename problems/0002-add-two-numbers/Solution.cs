using System.Diagnostics;
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     public int val;
 *     public ListNode next;
 *     public ListNode(int val=0, ListNode next=null) {
 *         this.val = val;
 *         this.next = next;
 *     }
 * }
 */
public class Solution {
    private ListNode AddDigits(ListNode l1, ListNode l2, int carry)
    {
        Debug.Assert(l1 != null || l2 != null, "Invalid State. Both list nodes are null");
        int value = carry + (l1?.val ?? 0) + (l2?.val ?? 0);
        int digitCarry = value / 10;
        int digitValue = value % 10;
        bool hasNextL1 = l1?.next != null;
        bool hasNextL2 = l2?.next != null;
        if (!hasNextL1 && !hasNextL2)
        {
            ListNode carryNode = digitCarry > 0 ? new ListNode(digitCarry) : null;
            return new ListNode(digitValue, carryNode);
        }
        return new ListNode(digitValue, this.AddDigits(l1?.next, l2?.next, digitCarry));
    }

    public ListNode AddTwoNumbers(ListNode l1, ListNode l2) {
        if (l1 == null && l2 == null)
        {
            return null;
        }
        if (l1 == null)
        {
            return l2;
        }
        if (l2 == null)
        {
            return l1;
        }
        return this.AddDigits(l1, l2, 0);
    }
}