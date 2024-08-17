import React, { useEffect, useRef } from "react";
import generateColors from "../utils/generateColors";

function NameWheel({ names }) {
    const canvasRef = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = Math.min(centerX, centerY) * 0.8; // Use 80% of available length
        const angleStep = (2 * Math.PI) / names.length; // divide 360 deg into parts of total available length

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const colors = generateColors(names.length);

        names.forEach((name, index) => {
            const startAngle = index * angleStep;
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
    }, [names]);

    return <canvas ref={canvasRef} width={600} height={600} />;
}

export default NameWheel;