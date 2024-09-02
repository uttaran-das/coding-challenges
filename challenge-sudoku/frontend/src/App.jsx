import React from 'react';
import './App.css';
import SudokuGrid from './components/SudokuGrid';

function App() {
  return (
    <div className="App">
      <h1>Sudoku Grid</h1>
      <SudokuGrid />
    </div>
  );
}

export default App;