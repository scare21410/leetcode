function calculatePalindrome(input: string, center: number) {
    for (let diff = 1; true; diff += 1) {
        if (input[center - diff] != input[center + diff]) {
            return input.slice(center - diff + 1, center + diff).split('#').join('');
        }
    }
}
/**
 * This is O(n*n), use Manarcher for O(n)
 */
export function longestPalindrome(s: string): string {
    if (s.length === 0) {
        return '';
    }
    let maxPalindrome = s[0];
    const augmentedInput = '^' + s.split('').join('#') + '$'

    for (let i = 1; i < augmentedInput.length - 1; i += 1) {
        const palindrome = calculatePalindrome(augmentedInput, i);
        if (palindrome.length > maxPalindrome.length) {
            maxPalindrome = palindrome;
        }
    }


    return maxPalindrome;
};