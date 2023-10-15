document.getElementById("login_btn").addEventListener('click', async () => {
    let email = document.getElementById("username").value;
    let password = document.getElementById("password").value;
    
    const url = 'http://127.0.0.1:5000/login';
    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "email": email, "password": password })
    };

    try {
        const response = await fetch(url, options);

        if (response.status === 200) {
            const authKey = response.headers.get('auth_key');  // Retrieve the authentication key from the response headers
            console.log('Authentication successful. Auth Key:', authKey);
        } else {
            console.error('Authentication failed');
        }
    } catch (error) {
        console.error(error);
    }
});
