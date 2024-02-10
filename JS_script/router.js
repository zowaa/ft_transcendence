const route = (event) => {
	event.preventDefault();
	window.history.pushState({}, "",event.target.href);
	handleLocations();
};

const routes = {
	404:		"/HTML_page/404.html",
	"/":		"/HTML_page/mrehba.html",
	"/hna":		"/HTML_page/hna.html",
	"/lhih":	"/HTML_page/lhih.html"
};

let initialLoad = true;
const handleLocations = async() => {
	const path = window.location.pathname;
	const routePath = routes[path] || routes[404];
	// if (!initialLoad) {
		const response = await fetch(routePath).then((response) => response.text());
		document.getElementById("body_to_load").innerHTML = response;
	// }
	// else {
	// 	initialLoad = false;
	// }
}

window.onpopstate = handleLocations;
window.route = route;
handleLocations();