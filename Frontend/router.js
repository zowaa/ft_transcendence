document.addEventListener("click", (e) => {
	const { target } = e;
	if (target.tagName === "A") {
		e.preventDefault();
		urlRoute(e);
	}
});


const urlPageTitle = "SPA router";
const urlRoutes = {

	404: {
		template: "/Frontend/Pages/404.html",
		title: "404 Not Found | " + urlPageTitle,
		description: "Page not found",
	},
	"/": {
		template: "/Frontend/Pages/home.html",
		title: "Home | " + urlPageTitle,
		description: "This is Home page",
	},
	"/about": {
		template: "/Frontend/Pages/about.html",
		title: "About | " + urlPageTitle,
		description: "This is About page",
	},
	"/contact_us": {
		template: "/Frontend/Pages/contact_us.html",
		title: "Contact_us | " + urlPageTitle,
		description: "This is Contact_us page",
	},
};


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
	const html = await fetch(route.template).then( (response) => response.text() );
	
	document.getElementById("body_to_load").innerHTML = html;
	document.title = route.title;
	document
		.querySelector('meta[name="description"]')
		.setAttribute("content", route.description);
};


window.onpopstate = urlLocationHandler;
window.onload = urlLocationHandler;
window.route = urlRoute;
urlLocationHandler();