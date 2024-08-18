import React from "react";
import '../styles/WinnerPopup.css'

function WinnerPopup({ name, onClose, onRemove }) {
    return (
        <div className="winner-popup">
            <div className="popup-content">
                <h2>We have a winner!</h2>
                <p>{name}</p>
                <button onClick={onClose}>Close</button>
                <button onClick={onRemove}>Remove</button>
            </div>
        </div>
    );
};

export default WinnerPopup;