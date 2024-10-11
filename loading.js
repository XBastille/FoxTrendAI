function restartCubeAnimation() {
    const cube = document.querySelector('.cube');
    const cubeEdges = cube.querySelectorAll('.cube-edge');
    cubeEdges.forEach(edge => {
        const clone = edge.cloneNode(true);
        edge.parentNode.replaceChild(clone, edge);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const grid = document.querySelector('.grid');
    const gridSize = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--grid-size'));
    const startX = grid.offsetWidth * 0.44; 
    const startY = grid.offsetHeight * 0.5; 
    
    function createWave() {
        let radius = 0;
        const maxRadius = Math.max(grid.offsetWidth, grid.offsetHeight);
        const interval = setInterval(() => {
            const innerRadius = radius - gridSize * 3;
            const outerRadius = radius;
            
            grid.querySelectorAll('.wave-cell').forEach(cell => cell.remove());
    
            for (let y = 0; y < grid.offsetHeight; y += gridSize) {
                for (let x = 0; x < grid.offsetWidth; x += gridSize) {
                    const distance = Math.sqrt(Math.pow(x - startX, 2) + Math.pow(y - startY, 2));
                    if (distance >= innerRadius && distance <= outerRadius) {
                        const cell = document.createElement('div');
                        cell.classList.add('wave-cell');
                        cell.style.left = `${x}px`;
                        cell.style.top = `${y}px`;
                        cell.style.width = `${gridSize}px`;
                        cell.style.height = `${gridSize}px`;
                        grid.appendChild(cell);
                    }
                }
            }
    
            radius += gridSize;
            if (radius > maxRadius) {
                clearInterval(interval);
                setTimeout(createWave, 8000 - (maxRadius / gridSize) * 50);
            }
        }, 50);
    }

    setTimeout(createWave, 4000);
    setInterval(restartCubeAnimation, 11600);
});


