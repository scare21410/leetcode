/**
 * Definition for singly-linked list.
 * type ListNode struct {
 *     Val int
 *     Next *ListNode
 * }
 */
func addDigits(l1 *ListNode, l2 *ListNode, carry int) *ListNode {
	if l1 == nil && l2 == nil {
		panic("Invalid state, both lists are nil")
	}
	l1Val := 0
	l2Val := 0

	if l1 != nil {
		l1Val = l1.Val
	}
	if l2 != nil {
		l2Val = l2.Val
	}
	value := carry + l1Val + l2Val
	digitCarry := value / 10
	digitValue := value % 10
	hasNextL1 := false
	hasNextL2 := false
	if l1 != nil && l1.Next != nil {
		hasNextL1 = true
	}
	if l2 != nil && l2.Next != nil {
		hasNextL2 = true
	}
	if !hasNextL1 && !hasNextL2 {
		var carryNode *ListNode
		if digitCarry > 0 {
			carryNode = &ListNode{Val: digitCarry}
		}
		return &ListNode{Val: digitValue, Next: carryNode}
	}
	var l1Next *ListNode
	if l1 != nil {
		l1Next = l1.Next
	}
	var l2Next *ListNode
	if l2 != nil {
		l2Next = l2.Next
	}
	return &ListNode{
		Val:  digitValue,
		Next: addDigits(l1Next, l2Next, digitCarry),
	}
}

func addTwoNumbers(l1 *ListNode, l2 *ListNode) *ListNode {
	if l1 == nil || l2 == nil {
		return nil
	}
	if l1 == nil {
		return l2
	}
	if l2 == nil {
		return l1
	}
	return addDigits(l1, l2, 0)
}
