import { isValidGrid } from "./CheckValidSudokuGrid";

/**
 * Solves a Sudoku puzzle represented as a 2D array of integers.
 * @param {Array} grid 2D array of integers representing the Sudoku puzzle.
 * @returns {Array|null} The solved puzzle if the puzzle is valid, or null if the puzzle is invalid.
 */
export function solveSudoku(grid) {
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
                    if (isValidGrid(grid, row, col, value)) {
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
