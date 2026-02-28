const MIN_INT_DIV_10 = ((1 << 31) / 10) >> 0;
const MAX_INT_DIV_10 = (~(1 << 31) / 10) >> 0;

export function reverse(x: number): number {
    let result = 0;
    let remainder = x;
    while (remainder !== 0) {
        // check for overflow before multiplying
        if (result < MIN_INT_DIV_10 || result > MAX_INT_DIV_10) {
            return 0;
        }
        result *= 10;
        result += remainder % 10;
        remainder = (remainder / 10) >> 0;
    }

    return result;
};