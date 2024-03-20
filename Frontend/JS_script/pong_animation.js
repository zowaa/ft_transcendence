
function runPongAnimation() {
    const canvas = document.getElementById('pongCanvas');
    const ctx = canvas.getContext('2d');

    let paddleWidth, paddleHeight, paddleMargin, ballSize, fontSize;
    let leftPaddleY, rightPaddleY;
    let scorePlayer1 = 0;
    let scorePlayer2 = 0;

	leftPaddleDirection = 1, rightPaddleDirection = -1;


    let balls; // Declare balls array here, but initialize it in resizeCanvas

    // Dynamic sizing
    function resizeCanvas() {
        canvas.width = window.innerWidth * 0.8;
        canvas.height = window.innerHeight * 0.6;

        paddleWidth = canvas.width * 0.02; // 2% of canvas width
        paddleHeight = canvas.height * 0.50; // 50% of canvas height
        paddleMargin = canvas.width * 0.02; 
        ballSize = canvas.width * 0.04; // Define ballSize here
        fontSize = canvas.width * 0.08; 

        // Initialize or re-initialize the balls array here
        balls = [
            { x: canvas.width / 2, y: canvas.height / 2, xSpeed: 2, ySpeed: 2, size: ballSize },
            { x: canvas.width / 2, y: canvas.height / 2, xSpeed: -2, ySpeed: 2, size: ballSize },
            { x: canvas.width / 2, y: canvas.height / 2, xSpeed: 2, ySpeed: -2, size: ballSize }
        ];

        leftPaddleY = canvas.height / 2 - paddleHeight / 2;
        rightPaddleY = canvas.height / 2 - paddleHeight / 2;
        
        draw(); // Redraw everything after resizing
    }

    // The rest of your functions (draw, animate, drawScore) should follow here.
    // No changes are needed in those parts for this specific issue resolution.
	// function drawScore() {
    //     ctx.font = `${fontSize}px 'Press Start 2P`;
    //     ctx.fillText(scorePlayer1.toString(), canvas.width / 4, fontSize);
    //     ctx.fillText(scorePlayer2.toString(), (3 * canvas.width) / 4, fontSize);
    // }



	function drawScore() {
		// Update the font size for larger text
		const scoreFontSize = fontSize + 20; // Increase the base fontSize by 20
		ctx.font = `${scoreFontSize}px 'Press Start 2P'`;
	
		// Calculate the y position to ensure visibility with the new font size
		const scorePosY = scoreFontSize * 1; // This ensures there's enough space at the top
	
		// Convert scores to string
		const score1Text = scorePlayer1.toString();
		const score2Text = scorePlayer2.toString();
	
		// Measure text width to centralize scores
		const score1Width = ctx.measureText(score1Text).width;
		const score2Width = ctx.measureText(score2Text).width;
	
		// Calculate x positions to place scores symmetrically around the middle line
		// Place scorePlayer1 to the left of the center
		const score1PosX = (canvas.width / 2) - score1Width - (ballSize * 2); // Adjust the spacing from the center as needed
		// Place scorePlayer2 to the right of the center
		const score2PosX = (canvas.width / 2) + (ballSize * 2); // Use the same spacing from the center as scorePlayer1
	
		// Draw scores with updated positions
		ctx.fillText(score1Text, score1PosX, scorePosY);
		ctx.fillText(score2Text, score2PosX, scorePosY);
	}




	function updateScores() {
        scorePlayer1 = Math.floor(Math.random() * 10);
        scorePlayer2 = Math.floor(Math.random() * 10);
    }

    // Draw paddles, balls, and scores
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = 'white';
        ctx.fillRect(paddleMargin, leftPaddleY, paddleWidth, paddleHeight);
        ctx.fillRect(canvas.width - paddleWidth - paddleMargin, rightPaddleY, paddleWidth, paddleHeight);

        // Draw each ball
        balls.forEach(ball => {
			// console.log(`Drawing ball at x: ${ball.x}, y: ${ball.y}, size: ${ball.size}`);
    
            ctx.fillRect(ball.x, ball.y, ball.size, ball.size);
        });

        ctx.beginPath();
        ctx.setLineDash([canvas.width * 0.005, canvas.width * 0.015]);
        ctx.moveTo(canvas.width / 2, 0);
        ctx.lineTo(canvas.width / 2, canvas.height);
        ctx.strokeStyle = 'white';
        ctx.stroke();

        drawScore();
    }

    function animate() {
		const normalizedPaddleSpeed = canvas.height * 0.007;
	
		leftPaddleY += leftPaddleDirection * normalizedPaddleSpeed;
		if (leftPaddleY <= 0 || leftPaddleY + paddleHeight >= canvas.height) {
			leftPaddleDirection *= -1; // Change direction
		}
	
		rightPaddleY += rightPaddleDirection * normalizedPaddleSpeed;
		if (rightPaddleY <= 0 || rightPaddleY + paddleHeight >= canvas.height) {
			rightPaddleDirection *= -1; // Change direction
		}
	
		// Dynamic speed adjustment based on canvas size
		const speedFactorX = canvas.width * 0.001; // Adjust these factors based on your game's needs
		const speedFactorY = canvas.height * 0.001;
	
		balls.forEach((ball, index) => {
			// Apply dynamic speed adjustment
			ball.x += ball.xSpeed * speedFactorX;
			ball.y += ball.ySpeed * speedFactorY;
	
			// Collision detection with top and bottom bounds
			if (ball.y <= 0 || (ball.y + ball.size) >= canvas.height) {
				ball.ySpeed *= -1;
			}
	
			// Enhanced collision detection with paddles
			if (ball.xSpeed < 0 && ball.x <= paddleMargin + paddleWidth && ball.x > paddleMargin && ball.y + ball.size > leftPaddleY && ball.y < leftPaddleY + paddleHeight) {
				ball.xSpeed *= -1;
				ball.x = paddleMargin + paddleWidth + 1; // Prevent sticking
			} else if (ball.xSpeed > 0 && ball.x + ball.size >= canvas.width - paddleWidth - paddleMargin && ball.x + ball.size < canvas.width - paddleMargin && ball.y + ball.size > rightPaddleY && ball.y < rightPaddleY + paddleHeight) {
				ball.xSpeed *= -1;
				ball.x = canvas.width - paddleWidth - paddleMargin - ball.size - 1; // Prevent sticking
			}
	
			// Reset ball if it goes out of bounds
			if (ball.x <= 0 || (ball.x + ball.size) >= canvas.width) {
				ball.x = canvas.width / 2 - ball.size / 2;
				ball.y = canvas.height / 2 - ball.size / 2;
	
				// Reapply unique speeds for variety upon reset
				switch (index) {
					case 0:
						ball.xSpeed = 2;
						ball.ySpeed = 2;
						break;
					case 1:
						ball.xSpeed = -2.5;
						ball.ySpeed = 2.5;
						break;
					case 2:
						ball.xSpeed = 3;
						ball.ySpeed = -3;
						break;
				}
			}
		});
	
		draw(); // Redraw everything
		requestAnimationFrame(animate); // Next animation frame
	}
	
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas(); // This initializes everything, including the balls array.

    setInterval(updateScores, 1500);
    animate(); // Start the animation loop.
}

