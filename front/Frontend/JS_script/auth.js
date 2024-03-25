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

            try {
                let response = await fetch('http://localhost/login/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: json,
                });

                if(response.ok) {
                    const responseData = await response.json();
                    localStorage.setItem('jwt', responseData.access);
                    window.history.pushState({}, "", '/profile'); 
                    urlLocationHandler();
                } else {
                    const errorResponse = await response.json(); // Parse the response to get the error object
                    if (errorResponse.error) {
                        // Iterate over the keys in the error object and create a message
                        let errorMessage = Object.keys(errorResponse.error)
                            .map(key => `${key}: ${errorResponse.error[key].join(", ")}`)
                            .join("\n");
                        alert(errorMessage);
                    } else {
                        alert("An unknown error occurred.");
                    }
                }
            } catch (error) {
                // Handle network errors or other unexpected errors
                console.error("Fetch error: ", error);
                alert("An error occurred while trying to communicate with the server.");
            }
        };
    }
}


//Sign-u
function attachSignupFormListener() {
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.onsubmit = async (event) => {
            event.preventDefault();

            let formDataObj = {};
            new FormData(signupForm).forEach((value, key) => formDataObj[key] = value);
            let jsonBody = JSON.stringify(formDataObj);

            try {
                let response = await fetch('http://localhost/register/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: jsonBody,
                });

                if (response.ok) {
                    const responseData = await response.json();
                    localStorage.setItem('jwt', responseData.access);
                    window.history.pushState({}, "", '/profile'); 
                    urlLocationHandler();
                } else {
                    const errorResponse = await response.json(); // Parse the response to get the error object
                    if (errorResponse.error) {
                        // Iterate over the keys in the error object and create a message
                        let errorMessage = Object.keys(errorResponse.error)
                            .map(key => `${key}: ${errorResponse.error[key].join(", ")}`)
                            .join("\n");
                        alert(errorMessage);
                    } else {
                        alert("An unknown error occurred.");
                    }
                }
            } catch (error) {
                // Handle network errors or other unexpected errors
                console.error("Fetch error: ", error);
                alert("An error occurred while trying to communicate with the server.");
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
                avatarElement.src = "Frontend/Assets/default.png";
            }
        } else {
            // Handle errors, e.g., by redirecting to the login page or showing an error message
            alert('Failed to load profile. Please try again.');
        }
    }
}
