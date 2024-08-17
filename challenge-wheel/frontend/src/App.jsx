import './App.css'
import { useState } from 'react';
import NameInput from './components/NameInput';
import { shuffle } from './utils/shuffleArray';
import NameWheel from './components/NameWheel';

function App() {
  const [names, setNames] = useState("");

  const handleChange = (e) => setNames(e.target.value);

  const handleShuffle = () => {
    const namesArray = names.split('\n');
    const shuffledArray = shuffle(namesArray);
    setNames(shuffledArray.join('\n'));
  };

  const handleSort = () => {
    const namesArray = names.split('\n');
    namesArray.sort();
    setNames(namesArray.join('\n'));
  };

  const filteredNames = names.split('\n').filter(name => name.trim() !== '');

  return (
    <div className="App">
      <div className="container">
        <div className="wheel-container">
          <NameWheel names={filteredNames} />
        </div>
        <div className="input-container">
          <h1>Name List</h1>
          <NameInput
            value={names}
            onChange={handleChange}
            onShuffle={handleShuffle}
            onSort={handleSort}
          />
        </div>
      </div>
    </div>
  );
}

export default App
