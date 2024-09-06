/**
 * Checks if a given Sudoku grid is valid.
 * A valid Sudoku grid is a 9x9 array of integers where each row, column, and 3x3 sub-grid contains the numbers 1-9 without repeating any number.
 * @param {Array} grid 2D array of integers representing the Sudoku puzzle.
 * @returns {boolean} True if the puzzle is valid, or false if it is invalid.
 */
export function validateSudoku(grid) {

    /**
     * Checks if a given array of numbers is valid, i.e. does not contain any duplicates or zeros.
     * @param {Array} arr Array of numbers to check.
     * @returns {boolean} True if the array is valid, or false if it is invalid.
     */
    const isValid = (arr) => arr.every((num, index, array) => array.indexOf(num) === index && num !== 0);

    // Checking rows
    for (let row = 0; row < 9; row++) {
        if (!isValid(grid[row])) return false;
    }

    // Checking columns
    for (let col = 0; col < 9; col++) {
        const column = grid.map(row => row[col]);
        if (!isValid(column)) return false;
    }

    // Checking 3x3 sub-grids
    for (let row = 0; row < 9; row += 3) for (let col = 0; col < 9; col += 3) {
        const subgrid = [];
        for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
            subgrid.push(grid[row + r][col + c]);
        }
        if (!isValid(subgrid)) return false;
    }

    return true;
}