export const generateColors = (count) => {
    const colors = [];
    for (let i = 0; i < count; i++) {
        colors.push(`hsl(${(i * 360) / count}, 100%, 50%)`);
    }
    return colors;
};

export default generateColors;