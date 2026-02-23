from typing import Optional
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

def addDigits(l1: Optional[ListNode], l2: Optional[ListNode], carry: int) -> ListNode:
    assert(l1 is not None or l2 is not None)
    value: int = carry + (l1.val if l1 is not None else 0) + (l2.val if l2 is not None else 0)
    digitCarry: int = value // 10
    digitValue: int = value % 10
    hasL1Next: bool = l1 is not None and l1.next is not None
    hasL2Next: bool = l2 is not None and l2.next is not None
    if not hasL1Next and not hasL2Next:
        carryNode = ListNode(digitCarry) if digitCarry > 0 else None
        return ListNode(digitValue, carryNode)
    return ListNode(
        digitValue, 
        addDigits(
            l1.next if hasL1Next else None, 
            l2.next if hasL2Next else None, 
            digitCarry
        )
    )

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        if l1 is None and l2 is None:
            return None
        if l1 is None:
            return l2
        if l2 is None:
            return l1
        
        return addDigits(l1, l2, 0)