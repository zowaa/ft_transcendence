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

    "/profile": {
		template: "/Frontend/Pages/profile.html",
		description: "This is the profile page",
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
	// if (location === '/' || location === '/Frontend/Pages/home.html') {
    //     runPongAnimation(); // Call a function to start the Pong animation.
    // }

	document
	.querySelector('meta[name="description"]')
	.setAttribute("content", route.description);
	
	attachSignupFormListener();
	attachLoginFormListener();
    fetchUserProfile();

	const init_lang = getSavedLanguagePreference();
	console.log(init_lang);
	const language = await import(`./Lang_files/lang.${init_lang}.js`);
	saveLanguagePreference(init_lang);
	applyLanguageToContent(language.default);
};

function attachSignupFormListener() {
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.onsubmit = async (event) => {
            event.preventDefault();

            // Create an object from the form entries
            let formDataObj = {};
            new FormData(signupForm).forEach((value, key) => formDataObj[key] = value);

            // Convert the object to a JSON string
            let jsonBody = JSON.stringify(formDataObj);

            let response = await fetch('http://localhost/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: jsonBody,
            });

            if (response.ok) { // Check if the response status is 2xx
                let result = await response.json();
                alert(result.message);
                // window.location.href = '/profile'; 
            } else {
                let errorResult = await response.json();
                alert(errorResult.detail || "An error occurred.");
            }
        };
    }
}

function attachLoginFormListener() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.onsubmit = async (event) => {
            event.preventDefault(); 

            let formData = new FormData(loginForm);
            // Converting FormData to JSON since we need to send JSON
            let object = {};
            formData.forEach((value, key) => {
                object[key] = value;
            });
            let json = JSON.stringify(object);

            let response = await fetch('http://localhost/login/', { // Change this URL to your login endpoint
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // Correctly setting Content-Type for JSON
                },
                body: json,
            });
            // if(response.ok) {
            //     let result = await response.json();
            //     alert(result.message); // Assuming the API responds with a message on successful login
            // } else {
            //     alert("Login failed. Please check your username and password.");
            // }
            if(response.ok) {
                const responseData = await response.json();
				// Store the JWT in localStorage
				localStorage.setItem('jwt', responseData.access);        
                // window.location.pathname = '/about'; 
                window.history.pushState({}, "", '/profile'); 
                urlLocationHandler();// Redirect to profile page
            } else {
                alert('Login failed: ');
            }
        };
        return false;
    }
}

async function fetchUserProfile() {
    const profile = document.getElementById('profile');
    if (profile) {
        const jwtToken = localStorage.getItem('jwt');  // Retrieve the JWT from localStorage
		if (!jwtToken) {
			console.error("JWT not found, user might not be logged in");
			return;
		}
        const response = await fetch('http://localhost/profile/', {
            method: 'GET', // Credentials (cookies) are included automatically
            // credentials: 'include', // This line is usually not necessary for same-origin requests
			headers: {
				'Authorization': `Bearer ${jwtToken}`,  // Include the JWT in the Authorization header
			},
        });

        if (response.ok) {
            const profileData = await response.json();
            console.log(profileData);
            
            // Update the page with the user's profile data
            document.getElementById('username').textContent = profileData.user.username || 'Unavailable';
			document.getElementById('status').textContent = profileData.user.status || 'Unavailable';

			const avatarUrl = profileData.user.avatar; // This should be the relative or absolute path to the avatar image
            const avatarElement = document.getElementById('avatar');
            if (avatarElement) {
                // Ensure your server gives the correct path to the image.
                // If it's a relative path, you might need to append the server's base URL.
                avatarElement.src = "Frontend/default.png";
            }
        } else {
            // Handle errors, e.g., by redirecting to the login page or showing an error message
            alert('Failed to load profile. Please try again.');
        }
    }
}

function getSavedLanguagePreference() {
    return localStorage.getItem("userLanguage") || "en";
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

window.onpopstate = urlLocationHandler;
window.onload = urlLocationHandler;


