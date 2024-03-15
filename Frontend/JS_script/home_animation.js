function runPongAnimation() {
    const canvas = document.getElementById('pongCanvas');
    const ctx = canvas.getContext('2d');

    // Dynamic sizing
    function resizeCanvas() {
        // Set canvas size based on window size
        canvas.width = window.innerWidth * 0.8;
        canvas.height = window.innerHeight * 0.6;

        // Update drawing sizes based on canvas size
        paddleWidth = canvas.width * 0.02; // 2% of canvas width
        paddleHeight = canvas.height * 0.35; // 35% of canvas height
        paddleMargin = canvas.width * 0.02; 
        ballSize = canvas.width * 0.05; 
        fontSize = canvas.width * 0.04; 

        leftPaddleY = canvas.height / 2 - paddleHeight / 2;
        rightPaddleY = canvas.height / 2 - paddleHeight / 2;
        ballX = canvas.width / 2 - ballSize / 2;
        ballY = canvas.height / 2 - ballSize / 2;
        
        draw(); // Redraw everything after resizing
    }

    let paddleWidth, paddleHeight, paddleMargin, ballSize, fontSize;
    let leftPaddleY, rightPaddleY, ballX, ballY;

    let scorePlayer1 = 0;
    let scorePlayer2 = 0;

	let leftPaddleSpeed = 2;
    let rightPaddleSpeed = -2;
	let ballXSpeed = 2;
    let ballYSpeed = 2;

    function drawScore() {
        ctx.font = `${fontSize}px Arial`; // dynamic font size
        ctx.fillText(scorePlayer1.toString(), canvas.width / 4, fontSize);
        ctx.fillText(scorePlayer2.toString(), (3 * canvas.width) / 4, fontSize);
    }

    // Draw paddles and ball
    function draw() {
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw left paddle
        ctx.fillRect(paddleMargin, leftPaddleY, paddleWidth, paddleHeight);

		ctx.fillStyle = 'white';
        // Draw right paddle
        ctx.fillRect(canvas.width - paddleWidth - paddleMargin, rightPaddleY, paddleWidth, paddleHeight);

        // Draw ball
        ctx.fillRect(ballX, ballY, ballSize, ballSize);

        // Draw middle dashed line
        ctx.beginPath();
        ctx.setLineDash([canvas.width * 0.005, canvas.width * 0.015]); // Dynamic dash size
        ctx.moveTo(canvas.width / 2, 0);
        ctx.lineTo(canvas.width / 2, canvas.height);
		ctx.strokeStyle = 'white';
        ctx.stroke();

        // Draw the scores
        drawScore();
    }

	function animate() {
        // Move the paddles
        leftPaddleY += leftPaddleSpeed;
        rightPaddleY += rightPaddleSpeed;


        ballX += ballXSpeed;
        ballY += ballYSpeed;

        // Check for top and bottom bounds and reverse speed if necessary
        if (leftPaddleY <= 0 || (leftPaddleY + paddleHeight) >= canvas.height) {
            leftPaddleSpeed *= -1;
        }

        if (rightPaddleY <= 0 || (rightPaddleY + paddleHeight) >= canvas.height) {
            rightPaddleSpeed *= -1;
        }


		if (ballY <= 0 || (ballY + ballSize) >= canvas.height) {
            ballYSpeed *= -1;
        }

        // Ball collision with paddles
        if (ballX <= paddleMargin + paddleWidth && ballY > leftPaddleY && ballY < leftPaddleY + paddleHeight) {
            ballXSpeed *= -1; // Reverse the ball's horizontal direction
        } else if (ballX >= canvas.width - paddleWidth - paddleMargin - ballSize && ballY > rightPaddleY && ballY < rightPaddleY + paddleHeight) {
            ballXSpeed *= -1; // Reverse the ball's horizontal direction
        }

        // Ball goes out of the left or right side
        if (ballX <= 0 || (ballX + ballSize) >= canvas.width) {
            // Reset ball to the center
            ballX = canvas.width / 2 - ballSize / 2;
            ballY = canvas.height / 2 - ballSize / 2;
            // You may want to reset the ball speed or reverse it
            // For example, reversing the horizontal speed to start play in the other direction
            ballXSpeed *= -1;
        }

        draw(); // Redraw everything

        requestAnimationFrame(animate); // Next animation frame
    }

    // Listen for window resize events
    window.addEventListener('resize', resizeCanvas);

    // Initial setup and draw
    resizeCanvas();
	animate();
}
