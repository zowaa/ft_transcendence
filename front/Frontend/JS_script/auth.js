// Sign-up
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
                    localStorage.setItem('logged_in', 'yes')
                    window.history.pushState({}, "", '/profile'); 
                    urlLocationHandler();
                } else {
                    const errorResponse = await response.json();
                    displayFormError_up(errorResponse.error);
                }
            } catch (error) {
                console.error("Fetch error: ", error);
                alert("An error occurred while trying to communicate with the server.");
            }
        };
    }
}

function displayFormError_up(errors) {
    // Reset previous errors
    resetErrorDisplay();

    // Display new errors
    if (errors) {
        for (const [field, messages] of Object.entries(errors)) {
            const errorElement = document.getElementById(`${field}`);
            if (errorElement) {
                errorElement.style.display = 'block';

                const inputElement = document.querySelector(`input[name="${field}"]`);
                if (inputElement) {
                    inputElement.style.marginBottom = '0px';
                }
            }
        }
    }
}

function resetErrorDisplay() {
    // Hide all error messages and reset input margins
    document.querySelectorAll('.text-danger').forEach(errorElement => {
        errorElement.style.display = 'none';
    });

    const xInput = document.querySelector('.x');
    const xxInput = document.querySelector('.xx');
    if (xInput) xInput.style.marginBottom = '20px';
    if (xxInput) xxInput.style.marginBottom = '40px';
}



// Sign-in
// function attachLoginFormListener() {
//     const loginForm = document.getElementById('loginForm');
//     if (loginForm) {
//         loginForm.onsubmit = async (event) => {
//             event.preventDefault(); 
//             let formData = new FormData(loginForm);
//             // Converting FormData to JSON since we need to send JSON
//             let object = {};
//             formData.forEach((value, key) => {
//                 object[key] = value;
//             });
//             let json = JSON.stringify(object);

//             try {
//                 let response = await fetch('http://localhost/login/', {
//                     method: 'POST',
//                     headers: {
//                         'Content-Type': 'application/json',
//                     },
//                     body: json,
//                 });

//                 if(response.ok) {
//                     const responseData = await response.json();
//                     localStorage.setItem('jwt', responseData.access);
//                     window.history.pushState({}, "", '/profile'); 
//                     urlLocationHandler();
//                 } else {
//                     const errorResponse = await response.json(); // Parse the response to get the error object
//                     if (errorResponse.error) {
//                         // Iterate over the keys in the error object and create a message
//                         let errorMessage = Object.keys(errorResponse.error)
//                             .map(key => `${key}: ${errorResponse.error[key].join(", ")}`)
//                             .join("\n");
//                         alert(errorMessage);
//                     } else {
//                         alert("An unknown error occurred.");
//                     }
//                 }
//             } catch (error) {
//                 // Handle network errors or other unexpected errors
//                 console.error("Fetch error: ", error);
//                 alert("An error occurred while trying to communicate with the server.");
//             }
//         };
//     }
// }


function attachLoginFormListener() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.onsubmit = async (event) => {
            event.preventDefault(); 

            let formData = new FormData(loginForm);
            let object = {};
            formData.forEach((value, key) => object[key] = value);
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
                    localStorage.setItem('logged_in', 'yes')
                    window.history.pushState({}, "", '/profile'); 
                    urlLocationHandler();
                } else {
                    const errorResponse = await response.json(); // Parse the response to get the error object
						displayFormError_in(errorResponse.error);
                }
            } catch (error) {
                // Handle network errors or other unexpected errors
                console.error("Fetch error: ", error);
                alert("An error occurred while trying to communicate with the server.");
            }
        };
    }
}

function displayFormError_in(errors) {
	// Reset previous errors
	resetErrorDisplay();

	// Display new errors
	if (errors) {
		for (const [field, messages] of Object.entries(errors)) {
			const errorElement = document.getElementById(`${field}`);
			if (errorElement) {
				// errorElement.textContent = messages.join(", ");
				errorElement.style.display = 'block';

				const inputElement = document.querySelector(`input[name="${field}"]`);
				if (inputElement) {
					inputElement.style.marginBottom = '0px';
				}
			}
		}
	}
}













function attachOAuthFormListener() {
    const signInButton = document.getElementById('btn2');
    if (signInButton) {
        signInButton.onclick = async (event) => {
            event.preventDefault();
            window.location.href = 'http://localhost/auth42/';
        };
    }
}



async function fetchUserProfile() {
    const profile = document.getElementById('profile');
    if (profile) {
        // Retrieve the JWT token from localStorage
        const jwtToken = localStorage.getItem('jwt');
        
        let headers = {};
        let fetchOptions = {
            method: 'GET',
            headers: headers,
        };

        // If JWT token is available, use it in the Authorization header
        if (jwtToken) {
            headers['Authorization'] = `Bearer ${jwtToken}`;
        } else {
            fetchOptions.credentials = 'include';
        }

        try {
            const response = await fetch('http://localhost/profile/', fetchOptions);

            if (response.ok) {
                const profileData = await response.json();
                console.log(profileData);

                // Update the page with the user's profile data
                // document.getElementById('username').textContent = profileData.user.username || 'Unavailable';
                // document.getElementById('status').textContent = profileData.user.status || 'Unavailable';
                
                // // Corrected the handling of the avatar element to update its 'src' attribute
                // const avatarElement = document.getElementById('avatar');
                // if (avatarElement) {
                //     avatarElement.src = profileData.user.avatar; // Use a default image if avatar URL is unavailable
                //     avatarElement.alt = "User Avatar"; // Ensuring the alt attribute is set for accessibility
                // }
            } else {
                // Handle non-OK responses, e.g., by displaying an error message
                alert('Failed to load profile. Please log in b3da.');
            }
        } catch (error) {
            console.error('Error fetching profile:', error);
            alert('An error occurred while trying to fetch the profile data.');
        }
    }
}

