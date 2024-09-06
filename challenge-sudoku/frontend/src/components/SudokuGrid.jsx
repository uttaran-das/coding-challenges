import React, { useEffect, useState } from 'react';
import { generateSudoku, removeCells } from '../utils/SudokuGenerator';

const SudokuGrid = () => {
  const [grid, setGrid] = useState(Array(9).fill(Array(9).fill('')));
  const [initialGrid, setInitialGrid] = useState(null);

  useEffect(() => {
    const solvedGrid = generateSudoku();
    const puzzleGrid = removeCells(solvedGrid);
    setGrid(puzzleGrid);
    setInitialGrid(puzzleGrid.map(row => row.slice()));
  }, []);

  const handleCellChange = (row, col, value) => {
    if (initialGrid[row][col] === 0) {
      const newGrid = grid.map(row => row.slice());
      newGrid[row][col] = value;
      setGrid(newGrid);
    }
  };

  const handleCellClear = (row, col) => {
    if (initialGrid[row][col] === 0) handleCellChange(row, col, 0);
  };

  if (!initialGrid) {
    return <div>Loading...</div>;
  }

  return (
    <div className="sudoku-grid">
      {grid.map((row, rowIndex) => (
        <div key={rowIndex} className="sudoku-row">
          {row.map((cell, colIndex) => (
            <input
              key={colIndex}
              type="text"
              className="sudoku-cell"
              value={cell === 0 ? '' : cell}
              onChange={(e) => {
                const value = e.target.value.slice(-1);
                if (/^[0-9]$/.test(value) || value === '') {
                  handleCellChange(rowIndex, colIndex, value === '' ? 0 : parseInt(value, 10));
                }
              }}
              onBlur={() => {
                if (cell === 0) {
                  handleCellClear(rowIndex, colIndex);
                }
              }}
              readOnly={initialGrid[rowIndex][colIndex] !== 0}
            />
          ))}
        </div>
      ))}
    </div>
  );
};

export default SudokuGrid;