/**
 * Checks whether a given value can be placed in a given cell in the Sudoku grid.
 * @param {Array} grid 2D array of integers representing the Sudoku puzzle.
 * @param {number} row Row index of the cell to check.
 * @param {number} col Column index of the cell to check.
 * @param {number} value Value to be placed in the cell.
 * @returns {boolean} True if the value can be placed in the cell, or false if it cannot.
 */
export const isValidGrid = (grid, row, col, value) => {
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