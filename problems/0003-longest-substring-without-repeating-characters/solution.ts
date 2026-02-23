export function lengthOfLongestSubstring(s: string): number {
  let maxLength = 0;
  let left = 0;
  let right = 0;
  const characterOccurence = new Set<number>();
  
  while (right < s.length) {
    const lastRightCharacterCode = s.charCodeAt(right);
    if (characterOccurence.has(lastRightCharacterCode)) {
        // we've found duplicate character, so we must not continue right, 
        // until we find the lastRightCharacterCode with left pointer, 
        // clearing characters as we go
        while (left < right) {
            const lastLeftCharacterCode = s.charCodeAt(left);
            characterOccurence.delete(lastLeftCharacterCode);
            left += 1;
            if (lastLeftCharacterCode === lastRightCharacterCode) {
                break;
            }
        }
    } else {
        // the current character is not yet in the map, 
        // let's add it and calculate max length
        characterOccurence.add(lastRightCharacterCode);
        maxLength = Math.max(maxLength, right - left + 1);
        right += 1
    }
  }

  return maxLength;
};