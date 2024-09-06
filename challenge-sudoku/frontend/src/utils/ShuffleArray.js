/**
 * Shuffles an array in place and returns the array.
 * @param {Array} array The array to shuffle.
 * @returns {Array} The shuffled array.
 */
export function shuffleArray(array) {
    // Loop through the array from the end to the beginning
    for (let i = array.length - 1; i > 0; i--) {
        // Generate a random index between 0 and the current index
        const j = Math.floor(Math.random() * (i + 1));
        // Swap the elements at the current index and the random index
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}