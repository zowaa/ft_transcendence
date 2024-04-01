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
				const response = await fetch('http://localhost/change_password/', {
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

//update username && 