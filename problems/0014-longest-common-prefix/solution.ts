function commonPrefix(w1: string, w2: string): string {
    let length = 0;
    const maxLength = Math.min(w1.length, w2.length);
    for (; length < maxLength; length += 1) {
        if (w1[length] !== w2[length]) {
            break;
        }
    }
    return w1.slice(0, length);
}
export function longestCommonPrefix(strs: string[]): string {
    let prefix = strs[0];
    for (let i = 1; i < strs.length; i += 1) {
        prefix = commonPrefix(prefix, strs[i]);
        if (prefix.length === 0) {
            return prefix;
        }
    }
    return prefix;
};