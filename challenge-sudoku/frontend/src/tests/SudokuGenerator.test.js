import { generateSudoku, removeCells } from '../utils/SudokuGenerator';
import { solveSudoku } from '../utils/SudokuSolver';
import { validateSudoku } from '../utils/SudokuValidator';

describe('generateSudoku', () => {
    it('should generate a valid Sudoku grid', () => {
        const grid = generateSudoku();
        console.log(grid);

        // Check that the grid is 9x9
        expect(grid.length).toBe(9);
        grid.forEach(row => {
            expect(row.length).toBe(9);
        });

        // Check that the grid is valid
        expect(validateSudoku(grid)).toBe(true);

        // Check that the grid can be solved
        const solvedGrid = solveSudoku(grid);
        expect(solvedGrid).toBeDefined();
        expect(solvedGrid.length).toBe(9);
        solvedGrid.forEach(row => {
            expect(row.length).toBe(9);
        });
    });
});

describe('removeCells', () => {
    it('should remove cells while ensuring the grid remains solvable', () => {
        const grid = generateSudoku();
        const originalGrid = grid.map(row => row.slice());

        removeCells(grid);

        // Check that some cells have been removed
        let removedCells = 0;
        for (let row = 0; row < 9; row++) {
            for (let col = 0; col < 9; col++) {
                if (grid[row][col] === 0) {
                    removedCells++;
                }
            }
        }
        expect(removedCells).toBeGreaterThan(0);

        // Check that the grid is still solvable
        const solvedGrid = solveSudoku(grid);
        expect(solvedGrid).toBeDefined();
        expect(solvedGrid.length).toBe(9);
        solvedGrid.forEach(row => {
            expect(row.length).toBe(9);
        });

        // Check that the solved grid matches the original grid
        for (let row = 0; row < 9; row++) {
            for (let col = 0; col < 9; col++) {
                if (originalGrid[row][col] !== 0) {
                    expect(solvedGrid[row][col]).toBe(originalGrid[row][col]);
                }
            }
        }
    });
});