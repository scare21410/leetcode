export function isPalindrome(x: number): boolean {
    if (x < 0) {
        return false;
    }
    if (x < 10) {
        return true;
    }
    if (x % 10 === 0) {
        return false;
    }
    const n = Math.ceil(Math.log10(x));
    const halfN = (n / 2) >> 0;
    let leftDecimals = Math.pow(10, n - 1);
    let rightDecimals = 1;
    for (let i = 0; i < halfN; i += 1) {
        const right = ((x / rightDecimals) >> 0)  % 10;
        const left = ((x / leftDecimals) >> 0) % 10;
        if (right !== left) {
            return false;
        }
        rightDecimals *= 10;
        leftDecimals = (leftDecimals / 10) >> 0;
    }
    return true;
}
