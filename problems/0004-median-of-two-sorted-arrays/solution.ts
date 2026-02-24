function kth(nums1: number[], nums2: number[], k: number): number {
    if (nums1.length === 0) {
        return nums2[k-1];
    }
    if (nums2.length === 0) {
        return nums1[k-1];
    }
    if (k === 1) {
        return Math.min(nums1[0], nums2[0]);
    }
    const midpoint = (k / 2) >> 0;
    const i = Math.min(nums1.length, midpoint);
    const j = Math.min(nums2.length, midpoint);
    return nums1[i - 1] < nums2[j - 1]
        ? kth(nums1.slice(i), nums2, k - i) // remove i elements from the start of the nums1 array
        : kth(nums1, nums2.slice(j), k - j) // remove j elements from the start of the nums2 array
}

export function findMedianSortedArrays(nums1: number[], nums2: number[]): number {
    const totalLength = nums1.length + nums2.length;
    const midpoint = (totalLength / 2) >> 0;
    return totalLength % 2 === 1
        ? kth(nums1, nums2, midpoint + 1)
        : (kth(nums1, nums2, midpoint) + kth(nums1, nums2, midpoint + 1)) / 2;
};
