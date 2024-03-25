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


//Sign-up
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

// //Oauth
// function attachOAuthFormListener() {
//     const loginButton = document.getElementById('btn2');
//     if (loginButton) {
//         loginButton.onclick = (event) => {
//             event.preventDefault();
//             // Option 1: Fetch the authorization URL from your backend
//             fetch('https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-78ad9702e59bae65f5d08c999f83b1a2e1b4bfccd90c7adabaab2faf0d71c2e0&')
//                 .then(response => response.json())
//                 .then(data => {
//                     alert("wach akhawa");
//                     const access = data.access;
//                     alert(access);
//                 })
//                 .catch(error => console.error('Error fetching auth URL:', error));

//             // Option 2: Redirect directly (hardcoded version, less secure)
//             // const authUrl = 'https://api.intra.42.fr/oauth/authorize?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_ENCODED_REDIRECT_URI&response_type=code&scope=public';
//             // window.location.href = authUrl;
//         }
//     }
// }

function attachOAuthFormListener() {
    const signInButton = document.getElementById('btn2');
    if (signInButton) {
        signInButton.onclick = async (event) => {
            event.preventDefault();
            // Directly navigate to the backend endpoint that initiates the OAuth flow
            window.location.href = 'http://localhost/auth42/';

            // let response = await fetch('https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-78ad9702e59bae65f5d08c999f83b1a2e1b4bfccd90c7adabaab2faf0d71c2e0&redirect_uri=http://localhost:8000/auth42_callback/&response_type=code&scope=public', {
            //     method: 'GET',
            //     headers: {
            //         'Accept': 'application/json',
            //     },
            // });

            // if (response.ok) { // Check if the response status is 2xx
            //     const responseData = await response.json();
			// 	// Store the JWT in localStorage
			// 	localStorage.setItem('jwt', responseData.access);        
            //     window.history.pushState({}, "", '/profile'); 
            //     urlLocationHandler(); // Redirect to profile page
            // } else {
            //     // Handle errors here, such as displaying an error message to the user.
            //     alert("An error occurred during the sign-in process.");
            // }
        };
    }
}

// function openOAuthWindow() {
//     // The URL to your OAuth endpoint that initiates the OAuth flow
//     const oauthUrl = 'http://localhost/auth42';

//     // Open a new window for the OAuth flow
//     const oauthWindow = window.open(oauthUrl, 'oauthWindow', 'width=500,height=600');

//     // Listen for a message from the window
//     window.addEventListener('message', (event) => {
//         // Make sure the message is from the OAuth window
//         if (event.source === oauthWindow) {
//             // Close the OAuth window
//             oauthWindow.close();

//             // Here you can handle the JWT token you expect to receive
//             // Assuming the message contains the JWT token in event.data.jwt
//             if (event.data && event.data.jwt) {
//                 // Store JWT token in local storage
//                 localStorage.setItem('jwt', event.data.jwt);

//                 // Redirect to the user's profile page or handle logged-in state as needed
//                 window.location.href = '/profile';
//             } else {
//                 // Handle error: no JWT in the message
//                 console.error('No JWT token received.');
//             }
//         }
//     }, false);
// }

// function attachOAuthFormListener() {
//     const signInButton = document.getElementById('btn2');
//     if (signInButton) {
//         signInButton.onclick = (event) => {
//             event.preventDefault();
//             openOAuthWindow(); // Call the function to open the OAuth window
//         };
//     }
// }




// document.getElementById('btn2').onclick = function() {
//     form.target = '_blank';
//     form.submit();
// }

async function fetchUserProfile() {
    const profile = document.getElementById('profile');
    if (profile) {
        // const jwtToken = localStorage.getItem('jwt');  // Retrieve the JWT from localStorage
		// if (!jwtToken) {
		// 	console.error("JWT not found, user might not be logged in");
		// 	return;
		// }
        const response = await fetch('https://localhost:8000/profile/', {
            method: 'GET', // Credentials (cookies) are included automatically
            // credentials: 'include', // This line is usually not necessary for same-origin requests
			// headers: {
			// 	'Authorization': `Bearer ${jwtToken}`,  // Include the JWT in the Authorization header
			// },
            credentials: 'include',
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
