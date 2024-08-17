// Fisher-Yates shuffle https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle

/*
Fisher-Yates shuffle is an efficient algorithm for randomly shuffling a sequence.

 It works by repeatedly swapping the current element with a randomly chosen element from the remaining unsorted portion. This ensures every permutation is equally likely. It's widely used in various applications due to its speed and unbiasedness.
*/

export const shuffle = (array) => {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

export default shuffle;