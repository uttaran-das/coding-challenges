import { shuffleArray } from './ShuffleArray';
import { isValidGrid } from './CheckValidSudokuGrid';
import { solveSudoku } from './SudokuSolver';

/**
 * Generates a valid Sudoku grid.
 * @returns {Array} 2D array of integers representing the Sudoku puzzle.
 */
export function generateSudoku() {
    /**
     * Recursively fills in the Sudoku grid with valid numbers.
     * @param {Array} grid 2D array of integers representing the Sudoku puzzle.
     * @returns {boolean} True if the puzzle can be solved, or false if it cannot.
     */
    const fillgrid = (grid) => {
        // Iterate over each cell in the grid.
        for (let row = 0; row < 9; row++)  for (let col = 0; col < 9; col++) {
            // If the cell is empty, try each possible value in the cell.
            if (grid[row][col] === 0) {
                const nums = [1, 2, 3, 4, 5, 6, 7, 8, 9];
                shuffleArray(nums);
                for (let num of nums) {
                    if (isValidGrid(grid, row, col, num)) {
                        grid[row][col] = num;
                        // If the puzzle can be solved with this value, return true.
                        if (fillgrid(grid)) return true;
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
    
    const grid = new Array(9).fill().map(() => new Array(9).fill(0));
    const success = fillgrid(grid);
    console.log(success);
    return grid;
}


/**
 * Removes random cells from a Sudoku grid while ensuring the puzzle remains solvable.
 *
 * @param {Array} grid - 2D array of integers representing the Sudoku puzzle.
 * @return {Array} The modified grid with random cells removed.
 */
export function removeCells(grid) {
    const copyGrid = (grid) => grid.map(row => row.slice());

    const originalGrid = copyGrid(grid);
    /**
     * Removes random cells from the Sudoku grid while ensuring the puzzle remains solvable.
     *
     * @param {Array} grid - 2D array of integers representing the Sudoku puzzle.
     * @param {number} attempts - The number of attempts to remove a cell. Defaults to 50.
     * @return {void} This function modifies the grid in place.
     */
    const removeRandomCells = (grid, attempts = 50) => {
        // Continue until we have tried to remove a cell `attempts` number of times.
        while (attempts > 0) {
            // Select a random cell from the grid.
            const row = Math.floor(Math.random() * 9);
            const col = Math.floor(Math.random() * 9);
            if (grid[row][col] !== 0) {
                // Store the current value in the cell, and reset the cell to 0.
                const num = grid[row][col];
                grid[row][col] = 0;
                // Create a copy of the grid and test if it is still solvable.
                const testGrid = copyGrid(grid);
                // If the puzzle is solvable, keep the cell as 0.
                if (solveSudoku(testGrid).some((row, r) => row.some((col, c) => col !== originalGrid[r][c]))) {
                    // If the puzzle is not solvable, reset the cell to the original value.
                    grid[row][col] = num;
                }
                // Decrement the number of attempts.
                attempts--;
            }
        }
    }

    removeRandomCells(grid);
    return grid;
}
