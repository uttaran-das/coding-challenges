function validateSudoku(grid) {

    const isValid = (arr) => arr.every((num, index, array) => array.indexOf(num) === index && num !== 0);

    // Checking rows
    for (let row = 0; row < 9; row++) {
        if (!isValid(grid[row])) return false;
    }

    // Checking columns
    for (let col = 0; col < 9; col++) {
        const column = grid.map(row => row[col]);
        if (!isValid(column)) return false;
    }

    // Checking 3x3 sub-grids
    for (let row = 0; row < 9; row += 3) for (let col = 0; col < 9; col += 3) {
        const subgrid = [];
        for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++) {
            subgrid.push(grid[row + r][col + c]);
        }
        if (!isValid(subgrid)) return false;
    }

    return true;
}

module.exports = validateSudoku;