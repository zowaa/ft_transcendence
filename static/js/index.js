let gameState = 'start'; 
let paddle_1 = document.querySelector('.paddle_1'); 
let paddle_2 = document.querySelector('.paddle_2'); 
let board = document.querySelector('.board'); 
let initial_ball = document.querySelector('.ball');
let ball = document.querySelector('.ball');
let score_1 = document.querySelector('.player_1_score');
let score_2 = document.querySelector('.player_2_score');
let name_1 = document.querySelector('.player_1_name');
let name_2 = document.querySelector('.player_2_name');
let message = document.querySelector('.message'); 
let paddle_1_coord = paddle_1.getBoundingClientRect(); 
let paddle_2_coord = paddle_2.getBoundingClientRect(); 
let initial_ball_coord = ball.getBoundingClientRect(); 
let ball_coord = initial_ball_coord;
let board_coord = board.getBoundingClientRect(); 
let paddle_common = 
	document.querySelector('.paddle').getBoundingClientRect(); 

let dx = Math.floor(Math.random() * 4) + 3; 
let dy = Math.floor(Math.random() * 4) + 3; 
let dxd = Math.floor(Math.random() * 2); 
let dyd = Math.floor(Math.random() * 2); 
let game_1 = ''
let game_2 = ''

let players = ["hamid1","hamid2","hamid3","hamid4"]







let gamefinalscore = 2;
let game1;
let game2;
let gamecounter = 0;
let final = [];
let Tournementid;
let winner;
const data = {
    player1: players[0],
    player2: players[1],
    player3: players[2],
    player4: players[3]
  };


  
//   // Make a POST request
fetch('http://127.0.0.1:8000/tournement/registre/', {
    method: 'POST',
    headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  }).then(response => {
    if (response.status === 201) {
      return response.json();
    } else {
      throw new Error(`Error: Status ${response.status}`);
    }
  }).then(data => {
    console.log(data);
    game1 = data.game1;
	game2 = data.game2;
	Tournementid = data.Tournementid;
	name_1.innerHTML = players[game1[0]];
	name_2.innerHTML = players[game1[1]];
  }).catch(error => {
    console.error('There was a problem with your fetch operation:', error);
    // redirect to the login here
  });

const eventx = document.addEventListener('keydown', (e) => {
if (e.key == 'Enter') {
	gameState = gameState == 'start' ? 'play' : 'start'; 
	if (gameState == 'play') {
	message.innerHTML = 'Tournement Game Started';
	message.style.left = 42 + 'vw'; 
	requestAnimationFrame(() => { 
		dx = Math.floor(Math.random() * 4) + 3; 
		dy = Math.floor(Math.random() * 4) + 3; 
		dxd = Math.floor(Math.random() * 2); 
		dyd = Math.floor(Math.random() * 2); 
		moveBall(dx, dy, dxd, dyd); 
	});
	}
}
if (gameState == 'play') { 
	if (e.key == 'w') { 
	paddle_1.style.top = 
		Math.max( 
		board_coord.top, 
		paddle_1_coord.top - window.innerHeight * 0.06 
		) + 'px'; 
	paddle_1_coord = paddle_1.getBoundingClientRect(); 
	} 
	if (e.key == 's') { 
	paddle_1.style.top = 
		Math.min( 
		board_coord.bottom - paddle_common.height, 
		paddle_1_coord.top + window.innerHeight * 0.06 
		) + 'px'; 
	paddle_1_coord = paddle_1.getBoundingClientRect(); 
	} 

	if (e.key == 'ArrowUp') { 
	paddle_2.style.top = 
		Math.max( 
		board_coord.top, 
		paddle_2_coord.top - window.innerHeight * 0.1 
		) + 'px'; 
	paddle_2_coord = paddle_2.getBoundingClientRect(); 
	} 
	if (e.key == 'ArrowDown') { 
	paddle_2.style.top = 
		Math.min( 
		board_coord.bottom - paddle_common.height, 
		paddle_2_coord.top + window.innerHeight * 0.1 
		) + 'px'; 
	paddle_2_coord = paddle_2.getBoundingClientRect(); 
	} 
} 
}); 

function moveBall(dx, dy, dxd, dyd) { 
if (ball_coord.top <= board_coord.top) { 
	dyd = 1; 
} 
if (ball_coord.bottom >= board_coord.bottom) { 
	dyd = 0; 
} 
if ( 
	ball_coord.left <= paddle_1_coord.right && 
	ball_coord.top >= paddle_1_coord.top && 
	ball_coord.bottom <= paddle_1_coord.bottom 
) { 
	dxd = 1; 
	dx = Math.floor(Math.random() * 4) + 3; 
	dy = Math.floor(Math.random() * 4) + 3; 
} 
if ( 
	ball_coord.right >= paddle_2_coord.left && 
	ball_coord.top >= paddle_2_coord.top && 
	ball_coord.bottom <= paddle_2_coord.bottom 
) { 
	dxd = 0; 
	dx = Math.floor(Math.random() * 4) + 3; 
	dy = Math.floor(Math.random() * 4) + 3; 
} 
if ( 
	ball_coord.left <= board_coord.left || 
	ball_coord.right >= board_coord.right 
) { 
	if (ball_coord.left <= board_coord.left) { 
	score_2.innerHTML = +score_2.innerHTML + 1; 
	} else { 
	score_1.innerHTML = +score_1.innerHTML + 1; 
	} 
	gameState = 'start'; 

	ball_coord = initial_ball_coord; 
	ball.style = initial_ball.style;
    if (score_1.innerHTML == gamefinalscore || score_2.innerHTML == gamefinalscore){
		gamecounter = gamecounter + 1;
		if (gamecounter == 3){
			// finish the tournement and annonce the winner
			gamecounter = 0;
			game1 = [];
			game2 = [];
			final = [];
			winner = '';
			if (score_1.innerHTML == gamefinalscore){
				message.innerHTML = 'The winner of the tournement : ' + name_1.innerHTML 
			}else {
				message.innerHTML = 'The winner of the tournement : ' + name_2.innerHTML 
			}
			name_1.innerHTML = ''
			name_2.innerHTML = ''
		} else {
			// print the right game announcement before every game
			if (gamecounter == 2){
				if (score_1.innerHTML == gamefinalscore){
					final[1] = name_1.innerHTML;
				}else {
					final[1] = name_2.innerHTML;
				}
				name_1.innerHTML = final[0];
        		name_2.innerHTML = final[1];
				message.innerHTML = 'Start the Tournement Final Game';
			} else if (gamecounter == 1){
				if (score_1.innerHTML == gamefinalscore){
					final[0] = name_1.innerHTML;
				}else {
					final[0] = name_2.innerHTML;
				}
				name_1.innerHTML = players[game2[0]];
        		name_2.innerHTML = players[game2[1]];
				message.innerHTML = 'Start the Tournement Game 2';
			}
		}
		score_1.innerHTML = 0;
    	score_2.innerHTML = 0;
    } else {
    	message.innerHTML = 'Press Enter to Play Pong'; 
    }
    // message.style.left = 38 + 'vw'; 
	return; 
} 
ball.style.top = ball_coord.top + dy * (dyd == 0 ? -1 : 1) + 'px'; 
ball.style.left = ball_coord.left + dx * (dxd == 0 ? -1 : 1) + 'px'; 
ball_coord = ball.getBoundingClientRect(); 
requestAnimationFrame(() => { 
	moveBall(dx, dy, dxd, dyd); 
}); 
} 
