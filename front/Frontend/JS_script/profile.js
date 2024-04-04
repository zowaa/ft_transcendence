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


// update username && display name
function updateUsername() {
	const updateUsernameForm = document.getElementById('update_info');
	if (updateUsernameForm) {
		let hadi;



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
					document.getElementById("avatar").disabled = true;
					document.getElementById("name").disabled = true;
					document.getElementById("disp_name").disabled = true;
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
						hadi = result.user.username;
					}
				}
				catch (error) {
					console.error(error);
					alert('An error occurred');
				}
			}
		}
		


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
					// alert(result.error);
					//display error
					display_error_up_form(result.error);
					
				} else {


					if (data.username !== hadi) {
						console.log(data.username, hadi);
						
						logout(); 
					} else {
						window.history.pushState({}, "", "/profile");
						urlLocationHandler(); 
					}

					// alert(result.message);
					//push
					// logout();
					// window.history.pushState({}, "", "/profile");
					// urlLocationHandler();
				}
			}
			catch (error) {
				console.error(error);
				alert('An error occurred');
			}
		}
	}
}

//display error
function display_error_up_form(error) {
	//print object in just alert key: field
	// alert(JSON.stringify(error));
	//rest error
	const sp1 = document.getElementById("display_name");
	const sp2 = document.getElementById("username");
	sp1.style.display = 'none';
	sp2.style.display = 'none';

	//display error
	if (error) {
		for(const [key, value] of Object.entries(error)) {
			const errorElement = document.getElementById(`${key}`);
			if (errorElement) {
				errorElement.style.display = 'block';
			}
		}
	}
}
	








async function fetchFriendships() {
    const jwtToken = localStorage.getItem('jwt');
    const jwtTokenCookie = getCookie('jwt');

    let headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    };
    if (jwtToken) {
        headers['Authorization'] = `Bearer ${jwtToken}`;
    } else if (jwtTokenCookie) {
        headers['Authorization'] = `Bearer ${jwtTokenCookie}`;
    }

    try {
        const response = await fetch('http://localhost:81/friends/', { 
            method: 'GET',
            headers: headers,
        });

        if (response.status === 200) {
            const data = await response.json();
            return data.friendships; 
        } else {
            console.error('Failed to fetch friendships', response.status);
            return []; 
        }
    } catch (error) {
        console.error('Error fetching friendships:', error);
        return []; 
    }
}

async function populateFriendsList() {

		const friendships = await fetchFriendships(); 
		const friendsListUl = document.querySelector('.friends-list ul');

		
		friendsListUl.innerHTML = '';

		friendships.forEach(friend => {
		
			const li = document.createElement('li');
			li.className = 'friend';

			
			const img = document.createElement('img');
			img.src = friend.avatar;
			img.className = 'avatarr';

			
			const div = document.createElement('div');
			div.className = 'friend-info';

			
			const h2 = document.createElement('h2');
			h2.className = 'friend-name';
			h2.textContent = friend.display_name;
			h2.style.color = 'black';

			
			const p = document.createElement('p');
			p.className = 'friend-status';
			p.textContent  = friend.status;
				
		
			
			div.appendChild(h2);
			div.appendChild(p);
			li.appendChild(img);
			li.appendChild(div);

		
			friendsListUl.appendChild(li);
    	});
	}










//add friend
function addFriend() {
	const addFriendForm = document.getElementById('add_friend');
	
	if (addFriendForm) {
		populateFriendsList();
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
					document.getElementById('msg3').style.display = 'block';
					
					
					await new Promise(r => setTimeout(r, 1000));
					
					window.history.pushState({}, "", "/friends");
					urlLocationHandler();
				}
				else {
					const result = await response.json();
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
    document.querySelectorAll('.text-danger').forEach(errorElement => {
        errorElement.style.display = 'none';
    });
}

// Update avatar

async function changeav() {
    const avatarInput = document.getElementById('avatar');
   

    const file = avatarInput.files[0];
    const formData = new FormData();
    formData.append('avatar', file);

    const jwtToken = localStorage.getItem('jwt');
    const jwtTokenCookie = getCookie('jwt');

    
    let headers = {};
    if (jwtToken) {
        headers['Authorization'] = `Bearer ${jwtToken}`;
    } else if (jwtTokenCookie) {
        headers['Authorization'] = `Bearer ${jwtTokenCookie}`;
    }

    try {
        const response = await fetch('http://localhost:82/avatar/', {
            method: 'POST',
            headers: headers, 
            body: formData,
        });
        const result = await response.json();
		if (result.status === 200) {
			window.history.pushState({}, "", "/profile");
			urlLocationHandler();
		}

       else {
            // alert(result.message);

			const span = document.getElementById("av_err");
			span.style.display = 'none';
			span.style.display = 'block';
        } 
    } catch (error) {
        console.error('An error occurred:', error);
        alert('An error occurred');
    }
}
