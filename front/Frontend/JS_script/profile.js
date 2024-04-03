//update password

function updatePassword() {
	const  updatePasswordForm = document.getElementById('update_pwd');
	if (updatePasswordForm) {
        updatePasswordForm.onsubmit = async function(e) {
			e.preventDefault();
			const jwtToken = localStorage.getItem('jwt');
			const jwtTokenCookie = getCookie('jwt');
			
			// let headers = {};
			let headers = {
                'Content-Type': 'application/json', // Set Content-Type header to application/json
            };
			if (jwtToken) {
				headers['Authorization'] = `Bearer ${jwtToken}`;
			} else if (jwtTokenCookie) {
				headers['Authorization'] = `Bearer ${jwtTokenCookie}`;
			}

			// const formData = new FormData(updatePasswordForm);
			const data = {
                old_password: updatePasswordForm.old_password.value,
                new_password: updatePasswordForm.new_password.value,
            };
			try {
				const response = await fetch('http://localhost:82/change_password/', {
					method: 'PUT',
					headers: headers,
					body: JSON.stringify(data),
				});
				const result = await response.json();
				if (result.error) {
					// alert(result.error);

					display_password_error(result.error);
					
				} else {
					// alert(result.message);
					//push
					window.history.pushState({}, "", "/settings");
					urlLocationHandler();
				}
			}
			catch (error) {
				console.error(error);
				alert('An error occurred');
			}
		}
	}
}


function display_password_error(error) {
	// resetErrorDisplay();
	document.querySelectorAll('.text-danger').forEach(errorElement => {
        errorElement.style.display = 'none';
    });

	if (error) {
		for(const [key, value] of Object.entries(error)) {
			const errorElement = document.getElementById(`${key}`);
			if (errorElement) {
				errorElement.style.display = 'block';

				// const inputElement = document.querySelector(`input[name="${key}"]`);
				// if (inputElement) {
				// 	inputElement.style.marginBottom = '0px';
				// }
			}
		}
	}
}



async function fetchAndPrefillUserInfo() {
    const myform = document.getElementById('update_info');
	if (myform) {
		const jwtToken = localStorage.getItem('jwt');
		const jwtTokenCookie = getCookie('jwt');
		let headers = {};
		if (jwtToken) {
			headers['Authorization'] = `Bearer ${jwtToken}`;
			//disable button
			
		} else if (jwtTokenCookie) {
			headers['Authorization'] = `Bearer ${jwtTokenCookie}`;
			document.getElementById("up").disabled = true;
			document.getElementById("bn").disabled = true;
			document.getElementById("avt").disabled = true;
		}
		try {
			const response = await fetch('http://localhost:82/profile/', {
				method: 'GET',
				headers: headers,
			});
			const result = await response.json();
			if (result.error) {
				alert(result.error);
			} else {
				myform.name.value = result.user.display_name;
				myform.disp_name.value = result.user.username;
			}
		}
		catch (error) {
			console.error(error);
			alert('An error occurred');
		}
	}
}


// update username && display name
function updateUsername() {
	const updateUsernameForm = document.getElementById('update_info');
	if (updateUsernameForm) {

		fetchAndPrefillUserInfo();


		updateUsernameForm.onsubmit = async function(e) {
			e.preventDefault();
			const jwtToken = localStorage.getItem('jwt');
			const jwtTokenCookie = getCookie('jwt');
			
			let headers = {
				'Content-Type': 'application/json', 
			};
			if (jwtToken) {
				headers['Authorization'] = `Bearer ${jwtToken}`;
			} else if (jwtTokenCookie) {
				headers['Authorization'] = `Bearer ${jwtTokenCookie}`;
			}

			const data = {
				username: updateUsernameForm.disp_name.value,
				display_name: updateUsernameForm.name.value,
			};
			try {
				const response = await fetch('http://localhost:82/profile/', {
					method: 'PUT',
					headers: headers,
					body: JSON.stringify(data),
				});
				const result = await response.json();
				if (result.error) {
					alert(result.error);
					
				} else {
					// alert(result.message);
					//push
					window.history.pushState({}, "", "/profile");
					urlLocationHandler();
				}
			}
			catch (error) {
				console.error(error);
				alert('An error occurred');
			}
		}
	}
}


//add friend
function addFriend() {
	const addFriendForm = document.getElementById('add_friend');
	if (addFriendForm) {
		addFriendForm.onsubmit = async function(e) {
			e.preventDefault();
			const jwtToken = localStorage.getItem('jwt');
			const jwtTokenCookie = getCookie('jwt');
			
			let headers = {
				'Content-Type': 'application/json', 
			};
			if (jwtToken) {
				headers['Authorization'] = `Bearer ${jwtToken}`;
			} else if (jwtTokenCookie) {
				headers['Authorization'] = `Bearer ${jwtTokenCookie}`;
			}

			const data = {
				username: addFriendForm.friend_name.value,
			};
			try {
				const response = await fetch('http://localhost:81/friends/', {
					method: 'POST',
					headers: headers,
					body: JSON.stringify(data),
				});

				if (response.status == 200) {
					// document.getElementById('msg3').style.color = 'green';
					document.getElementById('msg3').style.display = 'block';
					
					
					await new Promise(r => setTimeout(r, 1000));
					
					window.history.pushState({}, "", "/friends");
					urlLocationHandler();
				}
				else {
					const result = await response.json();
					// alert(result.message);
					display_friend_error(result.message);
				}
			}
			catch (error) {
				console.error(error);
				alert('An error occurred');
			}
		}
	}
}

function display_friend_error(error) {
	
	resetErrorDisplay_friend();
	if (error) {
		const errMsg = error;
		const errorElementId = `msg${errMsg.charAt(3)}`;
		const errorElement = document.getElementById(errorElementId);

		if (errorElement) {
            errorElement.style.display = 'block'; 
			
        }
	}


}

function resetErrorDisplay_friend() {
    // Hide all error messages and reset input margins
    document.querySelectorAll('.text-danger').forEach(errorElement => {
        errorElement.style.display = 'none';
    });

    // const xInput = document.querySelector('.x');
    // const xxInput = document.querySelector('.xx');
    // if (xInput) xInput.style.marginBottom = '20px';
    // if (xxInput) xxInput.style.marginBottom = '40px';
}