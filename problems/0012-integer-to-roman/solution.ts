const map = [
    ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX'],
    ['', 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC'],
    ['', 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM'],
    ['', 'M', 'MM', 'MMM'],
]

export function intToRoman(num: number): string {
    const parts = [];
    let order = 0;
    do {
        parts.push(map[order][num % 10]);
        num = (num / 10) >> 0;
        order += 1;
    } while (num > 0);

    return parts.reverse().join('');
};