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
    resetErrorDisplay();

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
    document.querySelectorAll('.text-danger').forEach(errorElement => {
        errorElement.style.display = 'none';
    });

    const xInput = document.querySelector('.x');
    const xxInput = document.querySelector('.xx');
    if (xInput) xInput.style.marginBottom = '20px';
    if (xxInput) xxInput.style.marginBottom = '40px';
}




// Sign-in
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
                    const errorResponse = await response.json(); 
						displayFormError_in(errorResponse.error);
                }
            } catch (error) {
                console.error("Fetch error: ", error);
                alert("An error occurred while trying to communicate with the server.");
            }
        };
    }
}

function displayFormError_in(errors) {
	resetErrorDisplay();

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





// OAuth
function attachOAuthFormListener() {
    const signInButton = document.getElementById('btn2');
    if (signInButton) {
        signInButton.onclick = async (event) => {
            event.preventDefault();
            sessionStorage.setItem('oauthAttempt', 'true');
            window.location.href = 'http://localhost/auth42/';
        };
    }
}



// check if user is logged in
function checkLoginStatus() { 
    const oauthAttempt = sessionStorage.getItem('oauthAttempt');
    const urlParams = new URLSearchParams(window.location.search);
    const loginSuccess = urlParams.get('success');

    if (loginSuccess === 'true' && oauthAttempt === 'true') {
        sessionStorage.removeItem('oauthAttempt');
        localStorage.setItem('logged_in', 'yes')
    } else if (oauthAttempt === 'true') {
        sessionStorage.removeItem('oauthAttempt');
    }
}

//get cookie
function getCookie(name) {
    let cookieArray = document.cookie.split(';');
    for(let i = 0; i < cookieArray.length; i++) {
        let cookiePair = cookieArray[i].split('=');
        if(name === cookiePair[0].trim()) {
            return decodeURIComponent(cookiePair[1]);
        }
    }
    return null; 
}


// Fetch user profile data
async function fetchUserProfile() {
    const profile = document.getElementById('kk');
    if (profile) {
        const jwtToken = localStorage.getItem('jwt');
        const jwtTokenCookie = getCookie('jwt');
        
        let headers = {};
        let fetchOptions = {
            method: 'GET',
            headers: headers,
        };

        if (jwtToken) {
            headers['Authorization'] = `Bearer ${jwtToken}`;
        } else if (jwtTokenCookie) {
            headers['Authorization'] = `Bearer ${jwtTokenCookie}`;
        }

        try {
            const response = await fetch('http://localhost:82/profile/', fetchOptions);

            if (response.ok) {
                const profileData = await response.json();

                document.getElementById('username').textContent ='@'+ profileData.user.username || 'Unavailable';
				document.getElementById('disp-n').textContent =  profileData.user.display_name || 'Unavailable';
                 const avatarElement = document.getElementById('avata');
                if (avatarElement) {
                    avatarElement.src = profileData.user.avatar;
                    avatarElement.alt = "User Avatar";
                }
                document.getElementById('wins-value').textContent = profileData.user.nb_wins || '0';
                document.getElementById('losses-value').textContent = profileData.user.nb_losses || '0';
            } else {
                alert('Failed to load profile. Please log in b3da.');
            }
        } catch (error) {
            console.error('Error fetching profile:', error);
            alert('An error occurred while trying to fetch the profile data.');
        }
    }
}










// Function to fetch and display the QR code for 2FA setup/verification
async function fetchQRCode() {
    const jwtToken = localStorage.getItem('jwt');
    const jwtTokenCookie = getCookie('jwt');
    
    let headers = {};
    let fetchOptions = {
        method: 'GET',
        headers: headers,
    };

    if (jwtToken) {
        headers['Authorization'] = `Bearer ${jwtToken}`;
    } else if (jwtTokenCookie) {
        headers['Authorization'] = `Bearer ${jwtTokenCookie}`;
    }
    try {
        const response = await fetch('http://localhost/qr_code/', fetchOptions);
        if (response.ok) {
            const imageUrl = URL.createObjectURL(await response.blob());
            document.getElementById('qrCodeImageContainer').innerHTML = `<img src="${imageUrl}" alt="QR Code">`;
        } else {
            alert('Failed to load QR code. Please try again.');
        }
    } catch (error) {
        console.error('Error fetching QR code:', error);
        alert('An error occurred. Please try again.');
    }
}

// Function to verify the code entered by the user
async function verifyCode() {
    const code = document.getElementById('verificationCode').value.trim();

    const jwtToken = localStorage.getItem('jwt');
    const jwtTokenCookie = getCookie('jwt');
    
    let headers = {
        'Content-Type': 'application/json'
    };

    if (jwtToken) {
        headers['Authorization'] = `Bearer ${jwtToken}`;
    } else if (jwtTokenCookie) {
        headers['Authorization'] = `Bearer ${jwtTokenCookie}`;
    }
    try {
        const response = await fetch('http://localhost/double_factor/', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({ code: code })
        });
        const data = await response.json();
        if (response.ok) {
            alert(data.message);
        } else {
            alert(data.message || 'Verification failed. Please try again.');
        }
    } catch (error) {
        console.error('Error verifying code:', error);
        alert('An error occurred. Please try again.');
    }
}

// Uncomment to test 2FA:

// fetchQRCode();
// verifyCode();

//logout
async function logout(){
	const jwtToken = localStorage.getItem('jwt');
    const jwtTokenCookie = getCookie('jwt');
    
    let headers = {};
    let fetchOptions = {
        method: 'POST',
        headers: headers,
    };

    if (jwtToken) {
        headers['Authorization'] = `Bearer ${jwtToken}`;
    } else if (jwtTokenCookie) {
        headers['Authorization'] = `Bearer ${jwtTokenCookie}`;
    }
    try {
        const response = await fetch('http://localhost/logout/', fetchOptions);
        if (response.ok) {
			document.cookie = "jwt=; expires" + new Date(0).toUTCString();
			localStorage.removeItem('jwt');

			localStorage.removeItem('logged_in');
			window.history.pushState({}, "", '/sign_in'); 
			urlLocationHandler();
		} else {
			alert('mabach ykhrej');
		}
}
catch (error) {
	console.error('Error logging out:', error);
	alert('An error occurred. Please try again.');
}
}