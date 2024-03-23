// Sign-in
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

            let response = await fetch('http://localhost/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: json,
            });

            if(response.ok) {
                const responseData = await response.json();
				// Store the JWT in localStorage
				localStorage.setItem('jwt',                                                                                                                                                                                                                                                                              .access);
                window.history.pushState({}, "", '/profile'); 
                urlLocationHandler();
            } else {
                alert('Login failed: ');
            }
        };
        return false;
    }
}

//Sign-u
function attachSignupFormListener() {
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.onsubmit = async (event) => {
            event.preventDefault();

            // Convert the object to a JSON string
            let formDataObj = {};
            new FormData(signupForm).forEach((value, key) => formDataObj[key] = value);
            let jsonBody = JSON.stringify(formDataObj);

            let response = await fetch('http://localhost/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: jsonBody,
            });

            if (response.ok) {
                const responseData = await response.json();
				// Store the JWT in localStorage
				localStorage.setItem('jwt', responseData.access);
                window.history.pushState({}, "", '/profile'); 
                urlLocationHandler();
            } else {
                let errorResult = await response.json();
                alert(errorResult.detail || "An error occurred.");
            }
        };
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
