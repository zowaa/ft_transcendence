function runGame() {
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');

    let paddleWidth, paddleHeight, paddleMargin, ballSize, fontSize, leftPaddleY, rightPaddleY, balls;
    let scorePlayer1 = 0, scorePlayer2 = 0, leftPaddleDirection = 1, rightPaddleDirection = -1;

    // Called when the window is resized && when the page is first loaded
    function resizeCanvas() {
        canvas.width = window.innerWidth * 0.8;
        canvas.height = window.innerHeight * 0.6;
        paddleWidth = canvas.width * 0.02; // 2%
        paddleHeight = canvas.height * 0.50; // 50%
        paddleMargin = canvas.width * 0.02; 
        ballSize = canvas.width * 0.04;
        fontSize = canvas.width * 0.08; 
		leftPaddleY = canvas.height / 2 - paddleHeight / 2;
		rightPaddleY = canvas.height / 2 - paddleHeight / 2;
        balls = [
            { x: canvas.width / 2, y: canvas.height / 2, xSpeed: 2, ySpeed: 2, size: ballSize },
            // { x: canvas.width / 2, y: canvas.height / 2, xSpeed: -2, ySpeed: 2, size: ballSize },
            // { x: canvas.width / 2, y: canvas.height / 2, xSpeed: 2, ySpeed: -2, size: ballSize }
        ];
        draw(); // Redraw everything after resizing
    }

	// Draw paddles, balls, scores and center line
	function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = 'white';
    	ctx.fillRect(paddleMargin, leftPaddleY, paddleWidth, paddleHeight); // Draw left paddle
        ctx.fillRect(canvas.width - paddleWidth - paddleMargin, rightPaddleY, paddleWidth, paddleHeight); // Draw right paddle
        balls.forEach(ball => {
            ctx.fillRect(ball.x, ball.y, ball.size, ball.size);
        }); // Draw each ball

		// Draw center line
        ctx.beginPath();
        ctx.setLineDash([canvas.width * 0.005, canvas.width * 0.015]);
        ctx.moveTo(canvas.width / 2, 0);
        ctx.lineTo(canvas.width / 2, canvas.height);
        ctx.strokeStyle = 'white';
        ctx.stroke();

        drawScore();
    }

	function drawScore() {
		const scoreFontSize = fontSize + 20;
		ctx.font = `${scoreFontSize}px 'Press Start 2P'`;
	
		const scorePosY = scoreFontSize;
	
		const score1Text = scorePlayer1.toString();
		const score2Text = scorePlayer2.toString();
	
		const score1Width = ctx.measureText(score1Text).width;
	
		const score1PosX = (canvas.width / 2) - score1Width - (ballSize * 2);
		const score2PosX = (canvas.width / 2) + (ballSize * 2); // Use the same spacing from the center as scorePlayer1
	
		ctx.fillText(score1Text, score1PosX, scorePosY);
		ctx.fillText(score2Text, score2PosX, scorePosY);
	}

    // function animate() {
	// 	const normalizedPaddleSpeed = canvas.height * 0.007;
	
	// 	// Move paddles
	// 	leftPaddleY += leftPaddleDirection * normalizedPaddleSpeed;
	// 	if (leftPaddleY <= 0 || leftPaddleY + paddleHeight >= canvas.height) {
	// 		leftPaddleDirection *= -1;
	// 	}
	// 	rightPaddleY += rightPaddleDirection * normalizedPaddleSpeed;
	// 	if (rightPaddleY <= 0 || rightPaddleY + paddleHeight >= canvas.height) {
	// 		rightPaddleDirection *= -1;
	// 	}

	// 	// Move balls
	// 	const speedFactorX = canvas.width * 0.001;
	// 	const speedFactorY = canvas.height * 0.001;
	
	// 	balls.forEach((ball, index) => {
	// 		ball.x += ball.xSpeed * speedFactorX;
	// 		ball.y += ball.ySpeed * speedFactorY;
	
	// 		// Collision with top and bottom bounds
	// 		if (ball.y <= 0 || (ball.y + ball.size) >= canvas.height) {
	// 			ball.ySpeed *= -1;
	// 		}
	
	// 		// Collision with paddles
	// 		if (ball.xSpeed < 0 && ball.x <= paddleMargin + paddleWidth && ball.x > paddleMargin && ball.y + ball.size > leftPaddleY && ball.y < leftPaddleY + paddleHeight) {
	// 			ball.xSpeed *= -1;
	// 			ball.x = paddleMargin + paddleWidth + 1;
	// 		} else if (ball.xSpeed > 0 && ball.x + ball.size >= canvas.width - paddleWidth - paddleMargin && ball.x + ball.size < canvas.width - paddleMargin && ball.y + ball.size > rightPaddleY && ball.y < rightPaddleY + paddleHeight) {
	// 			ball.xSpeed *= -1;
	// 			ball.x = canvas.width - paddleWidth - paddleMargin - ball.size - 1;
	// 		}
	
	// 		// Reset ball if it goes out of bounds
	// 		if (ball.x <= 0 || (ball.x + ball.size) >= canvas.width) {
	// 			ball.x = canvas.width / 2 - ball.size / 2;
	// 			ball.y = canvas.height / 2 - ball.size / 2;
	
	// 			switch (index) {
	// 				case 0:
	// 					ball.xSpeed = 2;
	// 					ball.ySpeed = 2;
	// 					break;
	// 				case 1:
	// 					ball.xSpeed = -2.5;
	// 					ball.ySpeed = 2.5;
	// 					break;
	// 				case 2:
	// 					ball.xSpeed = 3;
	// 					ball.ySpeed = -3;
	// 					break;
	// 			}
	// 		}
	// 	});
	
	// 	draw(); // Redraw everything
	// 	requestAnimationFrame(animate); // Next animation frame
	// }
	
	// function updateScores() {
    //     scorePlayer1 = Math.floor(Math.random() * 10);
    //     scorePlayer2 = Math.floor(Math.random() * 10);
    // }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // setInterval(updateScores, 1500);
    // animate(); // Start the animation loop.
}
