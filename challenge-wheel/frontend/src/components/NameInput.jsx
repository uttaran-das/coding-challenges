import React from "react";
import "../styles/NameInput.css";

function NameInput({ value, onChange, onShuffle, onSort }) {
    return (
        <div>
            <textarea
                rows="10"
                cols="30"
                value={value}
                onChange={onChange}
                placeholder="Enter names, one per line"
            />
            <div className="button-container">
                <button onClick={onShuffle}>Shuffle</button>
                <button onClick={onSort}>Sort</button>
            </div>
        </div>
    );
}

export default NameInput;