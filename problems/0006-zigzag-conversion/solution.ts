function processRow(s: string, numRows: number, row: number): string {
    const result: Array<string | undefined> = [];
    const isBorderline = row === 0 || row === numRows - 1;

    for (let i = 0; true; i += 1) {
        const index1 = row + i * 2 * (numRows - 1);
        const index2 = index1 + 2 * (numRows - 1 - row);

        const ch1 = s[index1];
        const ch2 = isBorderline ? undefined : s[index2];
        result.push(ch1);
        result.push(ch2);
        if (ch1 == undefined && ch2 == undefined) {
            return result.filter(Boolean).join('');
        }
    }
}

export function convert(s: string, numRows: number): string {
    return numRows > 1 
        ? [...new Array(numRows).keys()]
            .map((row) => processRow(s, numRows, row))
            .join('')
        : s;
};