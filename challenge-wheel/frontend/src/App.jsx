import './App.css'
import { useState } from 'react';
import NameInput from './components/NameInput';

function App() {
  const [names, setNames] = useState("");

  const handleChange = (e) => setNames(e.target.value);

  return (
    <div className="App">
      <h1>Name List</h1>
      <NameInput value={names} onChange={handleChange} />
      <div>
        <h2>Entered Names:</h2>
        <pre>{names}</pre>
      </div>
    </div>
  );
}

export default App
