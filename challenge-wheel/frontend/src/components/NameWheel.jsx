import React, { useEffect, useRef, useState } from "react";
import generateColors from "../utils/generateColors";
import WinnerPopup from "./WinnerPopup";
import '../styles/NameWheel.css'

function NameWheel({ names, onRemoveWinner }) {
    const canvasRef = useRef(null);
    const [isSpinning, setIsSpinning] = useState(false);
    const [rotation, setRotation] = useState(0);
    const [winnerIndex, setWinnerIndex] = useState(null);

    const angleStep = (2 * Math.PI) / names.length; // divide 360 deg into parts of total available length

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = Math.min(centerX, centerY) * 0.8; // Use 80% of available length

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const colors = generateColors(names.length);

        names.forEach((name, index) => {
            const startAngle = index * angleStep + rotation;
            const endAngle = startAngle + angleStep;

            // Segment
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, radius, startAngle, endAngle);
            ctx.closePath();
            ctx.fillStyle = colors[index];
            ctx.fill();
            ctx.strokeStyle = 'black';
            ctx.stroke();

            // Text
            ctx.save();
            ctx.translate(centerX, centerY);
            ctx.rotate(startAngle + angleStep / 2);
            ctx.textAlign = 'right';
            ctx.fillStyle = 'black';
            ctx.font = '14px Arial';
            ctx.fillText(name, radius * 0.75, 0);
            ctx.restore();
        });

        // Arrow indicator
        ctx.beginPath();
        ctx.moveTo(centerX, centerY - radius);
        ctx.lineTo(centerX - 10, centerY - radius - 20);
        ctx.lineTo(centerX + 10, centerY - radius - 20);
        ctx.closePath();
        ctx.fillStyle = 'red';
        ctx.fill();
        ctx.strokeStyle = 'black';
        ctx.stroke();
    }, [names, rotation]);

    const spinWheel = () => {
        setIsSpinning(true);
        setRotation(0);
        setWinnerIndex(null);

        let spinDuration = 4000; // 4 seconds
        let spinStartTime = performance.now();
        const targetWinnerIndex = Math.floor(Math.random() * names.length);
        let targetRotation = -(targetWinnerIndex + Math.random()) * angleStep - Math.PI / 2; // 90 deg offset for the arrow

        // ** The following if statement ensures that the targetRotation is always greater that rotation, this way the wheel will always rotate in clockwise direction
        if(targetRotation < rotation) {
            const diff = rotation - targetRotation;
            const divisor = Math.floor(diff / (2 * Math.PI));
            targetRotation += 2 * Math.PI * (divisor + 1) * Math.floor(5 + 5 * Math.random());
        }

        const animateSpin = (timestamp) => {
            const elapsed = timestamp - spinStartTime;
            const progress = Math.min(elapsed / spinDuration, 1);
            const easedProgress = 1 - Math.pow(1 - progress, 5); // ** 1 - (1 - x) ^ p

            let currentRotation = rotation + (targetRotation - rotation) * easedProgress;
            setRotation(currentRotation);

            if (progress < 1) {
                requestAnimationFrame(animateSpin);
            } else {
                // We should reduce the value of rotation once we done with a spin
                currentRotation -= Math.floor(currentRotation / (2 * Math.PI)) * 2 * Math.PI;
                setRotation(currentRotation);
                setIsSpinning(false);
                setWinnerIndex(targetWinnerIndex);
            }
        };

        requestAnimationFrame(animateSpin);
    };

    return (
        <div className="name-wheel">
            <canvas ref={canvasRef} width={500} height={500} />
            <button onClick={spinWheel} disabled={isSpinning || names.length === 0}>Spin</button>
            {winnerIndex !== null && (
                <WinnerPopup
                    name={names[winnerIndex]}
                    onClose={() => setWinnerIndex(null)}
                    onRemove={() => {
                        onRemoveWinner(names[winnerIndex]);
                        setWinnerIndex(null);
                    }}
                />
            )}
        </div>
    );
}

export default NameWheel;