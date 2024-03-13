function runPongAnimation() {
    const pong = document.getElementById('pong');
    const ball = document.querySelector('.ball');
    const leftPaddle = document.querySelector('.paddle.left');
    const rightPaddle = document.querySelector('.paddle.right');
    const score1 = document.getElementById('score1');
    const score2 = document.getElementById('score2');
    const pongRect = pong.getBoundingClientRect();

    let ballX = pongRect.width / 2, ballY = pongRect.height / 2;
    let ballXSpeed = 2, ballYSpeed = 2;
    let leftPaddleY = pongRect.height / 2 - pongRect.height * 0.15 / 2;
    let rightPaddleY = leftPaddleY;
    let leftPaddleDirection = 1, rightPaddleDirection = -1;
    let paddleHeight = pongRect.height * 0.15; // 15% of pong container height
    let paddleWidth = pongRect.width * 0.02; // 2% of pong container width
    let ballSize = pongRect.width * 0.02; // 2% of pong container width

    setInterval(() => {
        score1.textContent = Math.floor(Math.random() * 10);
        score2.textContent = Math.floor(Math.random() * 10);
    }, 1500);

    function update() {
        ballX += ballXSpeed;
        ballY += ballYSpeed;

        // Ball collision with top and bottom
        if (ballY <= 0 || ballY + ballSize >= pongRect.height) ballYSpeed *= -1;

        // Ball collision with paddles
        if (ballX <= paddleWidth && ballY + ballSize / 2 >= leftPaddleY && ballY - ballSize / 2 <= leftPaddleY + paddleHeight) {
            ballXSpeed *= -1;
        } else if (ballX + ballSize >= pongRect.width - paddleWidth && ballY + ballSize / 2 >= rightPaddleY && ballY - ballSize / 2 <= rightPaddleY + paddleHeight) {
            ballXSpeed *= -1;
        }

        // Reset ball if it passes paddles
        if (ballX < 0 || ballX > pongRect.width) {
            ballX = pongRect.width / 2;
            ballY = pongRect.height / 2;
            ballXSpeed = 2;
            ballYSpeed = 2;
        }

        // Move paddles
        leftPaddleY += leftPaddleDirection * 1; // Adjust speed as necessary
        rightPaddleY += rightPaddleDirection * 1; // Adjust speed as necessary

        // Paddles moving within boundaries
        if (leftPaddleY <= 0 || leftPaddleY + paddleHeight >= pongRect.height) {
            leftPaddleDirection *= -1;
        }

        if (rightPaddleY <= 0 || rightPaddleY + paddleHeight >= pongRect.height) {
            rightPaddleDirection *= -1;
        }

        // Update elements' positions
        ball.style.top = ballY + 'px';
        ball.style.left = ballX + 'px';
        leftPaddle.style.top = leftPaddleY + 'px';
        rightPaddle.style.top = rightPaddleY + 'px';

        requestAnimationFrame(update);
    }

    update();
}
