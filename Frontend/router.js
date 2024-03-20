const urlPageTitle = "SPA router";
const urlRoutes = {
	404: {
		template: "/Frontend/Pages/404.html",
		description: "Page not found",
	},
	"/": {
		template: "/Frontend/Pages/home.html",
		description: "This is Home page",
	},


	"/about": {
		template: "/Frontend/Pages/about.html",
		description: "This is About page",
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
    // localStorage.setItem("userLanguage", "en");
	if (location.length == 0) {
		location = "/";
	}

	


	const route = urlRoutes[location] || urlRoutes[404];
	// const html = await fetch(route.template).then((response) => response.text());
	
	const response = await fetch(route.template);

	let html;
	if(response.ok) {
		html = await response.text();
	} else {
		html = await fetch(urlRoutes[404].template).then((response) => response.text());
		console.error("Error: " + response.status);
	}

	
	document.getElementById("body_to_load").innerHTML = html;
	

	document
	.querySelector('meta[name="description"]')
	.setAttribute("content", route.description);
	
	const init_lang = getSavedLanguagePreference();
	console.log(init_lang);
	//print lang stored in local storage
console.log("mokk");
	// console.log("Language stored in local storage: " + init_lang);
	const language = await import(`./Lang_files/lang.${init_lang}.js`);
	saveLanguagePreference(init_lang);
	applyLanguageToContent(language.default);
	if (location === '/' || location === '/Frontend/Pages/home.html') {
        runPongAnimation();
    }
};

function getSavedLanguagePreference() {
    // return localStorage.getItem("userLanguage") || "fr";
	if (localStorage.getItem("userLanguage") === null) {
		console.log("3afak hna");
		console.log(localStorage.getItem("userLanguage"));
		return "en";
	}
	return localStorage.getItem("userLanguage") ;
}


function changeLanguage( selectedLanguage ) {
    // const selectedLanguage = document.getElementById("language").value;

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
    });

	if(lang.titles[window.location.pathname]){
		document.title = lang.titles[window.location.pathname];
	}
	else{
		document.title = lang.titles["404"];
	}
}




function setStars() {
	const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
	const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);

	function multipleBoxShadow(n) {
	  let shadows = [];
	  for (let i = 0; i < n; i++) {
		const x = Math.floor(Math.random() * vw) + 'px';
		const y = Math.floor(Math.random() * (vh + 2000)) - 1000 + 'px'; // Generate y values from -1000px to vh+1000px
		shadows.push(`${x} ${y} #FFF`);
	  }
	  return shadows.join(', ');
	}

	// Determine the number of stars based on the viewport width
	let starsSmall, starsMedium, starsLarge;
	if (vw <= 600) {
	  // Small devices
	  starsSmall = 300; // Adjust as needed
	  starsMedium = 100; // Adjust as needed
	  starsLarge = 50; // Adjust as needed
	} else if (vw <= 1200) {
	  // Medium devices
	  starsSmall = 500; // Adjust as needed
	  starsMedium = 150; // Adjust as needed
	  starsLarge = 75; // Adjust as needed
	} else {
	  // Large devices
	  starsSmall = 1000; // Adjust as needed
	  starsMedium = 500; // Adjust as needed
	  starsLarge = 300; // Adjust as needed
	}

	document.getElementById('stars').style.boxShadow = multipleBoxShadow(starsSmall);
	document.getElementById('stars2').style.boxShadow = multipleBoxShadow(starsMedium);
	document.getElementById('stars3').style.boxShadow = multipleBoxShadow(starsLarge);
  }
window.onpopstate = urlLocationHandler;
// window.onload = urlLocationHandler;

window.onload = () => {
    setStars();
    urlLocationHandler(); // Make sure to call the original onload function
};
window.onresize = setStars;


