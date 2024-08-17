import React from "react";

function NameInput({ value, onChange }) {
    return (
        <textarea
            rows="10"
            cols="30"
            value={value}
            onChange={onChange}
            placeholder="Enter names, one per line"
        />
    );
}

export default NameInput;