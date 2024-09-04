/**
 * Solves a Sudoku puzzle represented as a 2D array of integers.
 * @param {Array} grid 2D array of integers representing the Sudoku puzzle.
 * @returns {Array|null} The solved puzzle if the puzzle is valid, or null if the puzzle is invalid.
 */
function solveSudoku(grid) {
    /**
     * Checks whether a given value can be placed in a given cell in the Sudoku grid.
     * @param {Array} grid 2D array of integers representing the Sudoku puzzle.
     * @param {number} row Row index of the cell to check.
     * @param {number} col Column index of the cell to check.
     * @param {number} value Value to be placed in the cell.
     * @returns {boolean} True if the value can be placed in the cell, or false if it cannot.
     */
    const isValid = (grid, row, col, value) => {
        // Check that the value is not already present in the row or column.
        for (let x = 0; x < 9; x++) {
            if (grid[row][x] === value || grid[x][col] === value) return false;
        }
        // Check that the value is not already present in the 3x3 sub-grid.
        const startRow = Math.floor(row / 3) * 3;
        const startCol = Math.floor(col / 3) * 3;
        for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) {
            if (grid[startRow + i][startCol + j] === value) return false;
        }
        return true;
    }

    /**
     * Recursively solves the Sudoku puzzle by trying different values in each cell.
     * @returns {boolean} True if the puzzle can be solved, or false if it cannot.
     */
    const solve = () => {
        // Iterate over each cell in the grid.
        for (let row = 0; row < 9; row++) for (let col = 0; col < 9; col++) {
            // If the cell is empty, try each possible value in the cell.
            if (grid[row][col] === 0) {
                for (let value = 1; value <= 9; value++) {
                    if (isValid(grid, row, col, value)) {
                        grid[row][col] = value;
                        // If the puzzle can be solved with this value, return true.
                        if (solve()) return true;
                        // If the puzzle cannot be solved with this value, reset the cell to 0.
                        grid[row][col] = 0;
                    }
                }
                // If no valid values can be placed in the cell, return false.
                return false;
            }
        }
        // If all cells have been filled in, return true.
        return true;
    }

    // Solve the puzzle and return the result.
    return solve() ? grid : null;
}

module.exports = solveSudoku;