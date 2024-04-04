function setStars() {
	const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
	const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);

	function multipleBoxShadow(n) {
		let shadows = [];
		for (let i = 0; i < n; i++) {
			const x = Math.floor(Math.random() * vw) + 'px'; // pos_x : 0 to the viewport width 
			const y = Math.floor(Math.random() * (vh + 2000)) - 1000 + 'px'; // pos_y : -1000px to vh+1000px
			shadows.push(`${x} ${y} #FFF`);
		}
		return shadows.join(', ');
	}

	// Determine stars nb
	let starsSmall, starsMedium, starsLarge;
	if (vw <= 500) {
	  starsSmall = 300;
	  starsMedium = 100;
	  starsLarge = 50;
	}
	else if (vw <= 1300) {
	  starsSmall = 500;
	  starsMedium = 150;
	  starsLarge = 75;
	}
	else {
	  starsSmall = 1000;
	  starsMedium = 500;
	  starsLarge = 300;
	}

	document.getElementById('stars').style.boxShadow = multipleBoxShadow(starsSmall);
	document.getElementById('stars2').style.boxShadow = multipleBoxShadow(starsMedium);
	document.getElementById('stars3').style.boxShadow = multipleBoxShadow(starsLarge);
}


function go_home() {
	window.history.pushState({}, "", "/");
	urlLocationHandler();
}