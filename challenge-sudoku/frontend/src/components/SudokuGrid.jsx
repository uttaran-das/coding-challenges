import React, { useState } from 'react';

const SudokuGrid = () => {
  const [grid, setGrid] = useState(Array(9).fill(Array(9).fill('')));

  const handleCellChange = (row, col, value) => {
    const newGrid = grid.map(row => row.slice());
    newGrid[row][col] = value;
    setGrid(newGrid);
  };

  const handleCellClear = (row, col) => {
    handleCellChange(row, col, '');
  };

  return (
    <div className="sudoku-grid">
      {grid.map((row, rowIndex) => (
        <div key={rowIndex} className="sudoku-row">
          {row.map((cell, colIndex) => (
            <input
              key={colIndex}
              type="text"
              className="sudoku-cell"
              value={cell}
              onChange={(e) => {
                const value = e.target.value.slice(-1);
                if (/^[0-9]$/.test(value) || value === '') {
                  handleCellChange(rowIndex, colIndex, value);
                }
              }}
              onBlur={() => {
                if (cell === '') {
                  handleCellClear(rowIndex, colIndex);
                }
              }}
            />
          ))}
        </div>
      ))}
    </div>
  );
};

export default SudokuGrid;