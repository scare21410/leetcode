const INT_MIN = 1 << 31;
const INT_MAX = ~INT_MIN;

export function myAtoi(s: string): number {
    let i = 0;
    while (s[i] === ' ') {
        i += 1;
    }
    const negative = s[i] === '-';
    if (s[i] === '-' || s[i] === '+') {
        i += 1;
    }
    let result = 0;
    while (s[i] >= '0' && s[i] <= '9') {
        result *= 10;
        result += s.charCodeAt(i) - '0'.charCodeAt(0);
        i += 1;
    }
    return Math.min(INT_MAX, Math.max(INT_MIN, negative ? -result : result));
};