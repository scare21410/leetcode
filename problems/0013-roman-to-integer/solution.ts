export function romanToInt(s: string): number {
    let result = 0;
    for (let i = 0; i < s.length; i += 1) {
        switch (true) {
            case s[i] === 'I' && s[i + 1] === 'V':
                result += 4;
                i += 1;
                break;
            case s[i] === 'I' && s[i + 1] === 'X':
                result += 9;
                i += 1;
                break;
            case s[i] === 'X' && s[i + 1] === 'L':
                result += 40;
                i += 1;
                break;
            case s[i] === 'X' && s[i + 1] === 'C':
                result += 90;
                i += 1;
                break;
            case s[i] === 'C' && s[i + 1] === 'D':
                result += 400;
                i += 1;
                break;
            case s[i] === 'C' && s[i + 1] === 'M':
                result += 900;
                i += 1;
                break;
            case s[i] === 'I':
                result += 1;
                break;
            case s[i] === 'V':
                result += 5;
                break;
            case s[i] === 'X':
                result += 10;
                break;
            case s[i] === 'L':
                result += 50;
                break;
            case s[i] === 'C':
                result += 100;
                break;
            case s[i] === 'D':
                result += 500;
                break;
            case s[i] === 'M':
                result += 1000;
                break;
        }
    }
    return result;
}
