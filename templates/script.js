// Get the ball element
var ball = document.getElementById('ball');

// Listen for animation iteration event
ball.addEventListener('animationiteration', function() {
    // Reset the ball position to start
    ball.style.top = '50%';
    ball.style.left = '10%';
});
