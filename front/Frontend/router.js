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


	"/2fa": {
		template: "/Frontend/Pages/2fa.html",
		description: "This is the 2fa page",
	},

	


	"/contact_us": {
		template: "/Frontend/Pages/contact_us.html",
		description: "This is Contact_us page",
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

	const location = window.location.pathname;
	if (location.length == 0) {
		location = "/";
	}

	const route = urlRoutes[location] || urlRoutes[404];
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
	checkLoginStatus();

	const init_lang = getSavedLanguagePreference();
	const language = await import(`./Lang_files/lang.${init_lang}.js`);
	saveLanguagePreference(init_lang);
	applyLanguageToContent(language.default);

	if (location === '/') {
        runPongAnimation();
    }
	if (location === '/game') {
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