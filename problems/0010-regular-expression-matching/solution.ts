type Char = {
    type: 'char';
    char: string;
    repeated: boolean;
}
type Placeholder = {
    type: 'placeholder';
    repeated: boolean;
}
type PatternPart = Char | Placeholder;
type Pattern = readonly PatternPart[];

function parsePattern(p: string): Pattern {
    const result: PatternPart[] = [];
    for (let i = 0; i < p.length; i += 1) {
        switch (true) {
            case p[i + 1] === '*':
                result.push(
                    p[i] === '.' 
                        ? { type: 'placeholder', repeated: true }
                        : { type: 'char', char: p[i], repeated: true }
                );
                i += 1;
                break;

            default:
                result.push(
                    p[i] === '.' 
                        ? { type: 'placeholder', repeated: false }
                        : { type: 'char', char: p[i], repeated: false }
                );
                break;
        }
    }
    return result;
}

function isPatternPartCompatible(left: PatternPart, right: PatternPart): boolean {
    return left.repeated && 
        right.repeated && 
        left.type === 'char' &&  
        right.type === 'char' && 
        left.char === right.char || 
            
        left.repeated && 
        right.repeated &&
        left.type === 'placeholder' &&
        right.type === 'placeholder';
}

function optimisePattern(p: Pattern): Pattern {
    const result = [...p];
    let i = 0;
    while (i < result.length) {
        if (result[i] && result[i + 1] && isPatternPartCompatible(result[i], result[i + 1])) {
            result.splice(i + 1, 1);
        } else {
            i += 1;
        }
    }
    return result;
}

function matchesChar(char: string, pp: PatternPart): boolean {
    if (pp.type === 'placeholder') {
        return true;
    }
    if (pp.type === 'char') {
        return pp.char === char;
    }
    return false; // we should never get here
}

function matchPattern(s: string, p: readonly PatternPart[] = []): boolean {
    if (s.length === 0) {
        return p.every((pp) => pp.repeated); // we may have multiple .* at the end of the pattern
    }
    if (p.length === 0) {
        return s.length === 0;
    }
    const [head, ...tail] = p;
    if (!matchesChar(s[0], head)) {
        return head.repeated 
            ? matchPattern(s, tail) // repeated patterns may mean 0 occurences, so check if we can skip head
            : false;
    };
    return head.repeated
        ? matchPattern(s.slice(1), p) || matchPattern(s.slice(1), tail) || matchPattern(s, tail)
        : matchPattern(s.slice(1), tail);
}

export function isMatch(s: string, p: string): boolean {
    const pattern = optimisePattern(parsePattern(p));
    return matchPattern(s, pattern);
}
