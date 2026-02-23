struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};

ListNode* addDigits(ListNode* l1, ListNode* l2, unsigned int carry) {
    assert(l1 || l2);
    unsigned int value = carry + (l1 ? l1->val : 0) + (l2 ? l2->val : 0);
    unsigned int digitCarry = value / 10;
    unsigned int digitValue = value % 10;
    bool hasNextL1 = l1 != nullptr && l1->next != nullptr;
    bool hasNextL2 = l2 != nullptr && l2->next != nullptr;
    if (!hasNextL1 && !hasNextL2) {
        auto carryNode = digitCarry ? new ListNode(digitCarry) : nullptr;
        return new ListNode(digitValue, carryNode);
    }
    return new ListNode(
        digitValue, 
        addDigits(
            hasNextL1 ? l1->next : nullptr, 
            hasNextL2 ? l2->next : nullptr, 
            digitCarry
        )
    );
}

class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        if (!l1 && !l2) {
            return nullptr;
        }
        if (!l1) {
            return l2;
        }
        if (!l2) {
            return l1;
        }

        return addDigits(l1, l2, 0);
    }
};