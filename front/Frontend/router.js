const urlRoutes = {
	404: {
		template: "/Frontend/Pages/404.html",
		description: "Page not found",
	},
	"/": {
		template: "/Frontend/Pages/home.html",
		description: "This is Home page",
	},
	"/sign_in": {
		template: "/Frontend/Pages/sign_in.html",
		description: "This is Sign_in page",
	},
	"/sign_up": {
		template: "/Frontend/Pages/sign_up.html",
		description: "This is Sign_up page",
	},
	"/game": {
		template: "/Frontend/Pages/game.html",
		description: "This is Game page",
	},
	"/profile": {
		template: "/Frontend/Pages/profile.html",
		description: "This is the profile page",
	},
	"/game_b": {
		template: "/Frontend/Pages/game_b.html",
		description: "This is the game_b page",
	},
	"/settings": {
		template: "/Frontend/Pages/settings.html",
		description: "This is the settings page",
	},
	"/go_pwd": {
		template: "/Frontend/Pages/go_pwd.html",
		description: "This is the go_pwd page",
	},
	"/friends": {
		template: "/Frontend/Pages/friends.html",
		description: "This is the friends page",
	},
	"/history": {
		template: "/Frontend/Pages/history.html",
		description: "This is the history page",
	},
	


	"/2fa": {
		template: "/Frontend/Pages/2fa.html",
		description: "This is the 2fa page",
	},


};


document.addEventListener("click", (e) => {
    const { target } = e;
    if (target.tagName === "A") {
        e.preventDefault();
        urlRoute(e);
    }
});



const urlRoute = (event) => {
	event.preventDefault();
	window.history.pushState({}, "", event.target.href);
	urlLocationHandler();
};

const urlLocationHandler = async () => {

	let locationn = window.location.pathname;
	if (locationn.length == 0) {
		locationn = "/";
	}

	checkLoginStatus();
	const status = localStorage.getItem('logged_in');
	if (status === 'yes' && (locationn === '/sign_in' || locationn === '/sign_up')){
		// alert("You are already logged in");
		locationn = "/profile";
		//change pathname
		window.history.pushState({}, "", "/profile");
		urlLocationHandler();
		console.log("You are already logged in");
	}
	else if (status !== 'yes' && (locationn === '/profile' || locationn === '/game' || locationn === '/friends' || locationn === '/settings' || locationn === '/go_pwd' || locationn === '/history')){
		// alert("You need to be logged in to access this page");
		locationn = "/sign_in";
		//change pathname
		window.history.pushState({}, "", "/sign_in");
		urlLocationHandler();
		console.log("You need to be logged in to access this page");
	}



	const route = urlRoutes[locationn] || urlRoutes[404];
	const response = await fetch(route.template);

	let html;
	if(response.ok) {
		html = await response.text();
	} else {
		html = await fetch(urlRoutes[404].template).then((response) => response.text());
		console.error("Error: " + response.status);
	}

	document.getElementById("body_to_load").innerHTML = html;
	document.querySelector('meta[name="description"]').setAttribute("content", route.description);
	
	//auth functions
	attachSignupFormListener();
	attachLoginFormListener();
    fetchUserProfile();
	attachOAuthFormListener();
	// checkLoginStatus();
	updatePassword();
	updateUsername();
	addFriend();
	// fetchAndPrefillUserInfo();

	const init_lang = getSavedLanguagePreference();
	const language = await import(`./Lang_files/lang.${init_lang}.js`);
	saveLanguagePreference(init_lang);
	applyLanguageToContent(language.default);

	if (locationn === '/') {
        runPongAnimation();
    }
	if (locationn === '/game') {
		runGame();
	}
};

function getSavedLanguagePreference() {
	return localStorage.getItem("userLanguage") || "en";
}


function changeLanguage( selectedLanguage ) {
    loadLanguage(selectedLanguage);
}

async function loadLanguage(language) {
	const langModule = await import(`./Lang_files/lang.${language}.js`);
	saveLanguagePreference(language);
	applyLanguageToContent(langModule.default);
}

function saveLanguagePreference(language) {
    localStorage.setItem("userLanguage", language);
}

function applyLanguageToContent(lang) {
    const elementsToTranslate = document.querySelectorAll('[data-i18n]');
    
    elementsToTranslate.forEach((element) => {
        const key = element.getAttribute('data-i18n');
        element.textContent = lang[key] || '';
		if (element.tagName === "INPUT") {
			element.placeholder = lang.placeholders[key] || '';
		}
    });

	if(lang.titles[window.location.pathname]){
		document.title = lang.titles[window.location.pathname];
	}
	else{
		document.title = lang.titles["404"];
	}
}

window.onpopstate = urlLocationHandler;

window.onload = () => {
    setStars();
    urlLocationHandler();
};

window.onresize = () => {
	setStars();
} 

function add_pr() {
	window.history.pushState({}, "", "/profile");
	urlLocationHandler();
}

function add_gm() {
	window.history.pushState({}, "", "/game_b");
	urlLocationHandler();
}
function add_st() {
	window.history.pushState({}, "", "/settings");
	urlLocationHandler();
}

function go_pwd() {
	window.history.pushState({}, "", "/go_pwd");
	urlLocationHandler();
}

function add_fr() {
	window.history.pushState({}, "", "/friends");
	urlLocationHandler();
}
function add_hs() {
	window.history.pushState({}, "", "/history");
	urlLocationHandler();
}