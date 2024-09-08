<script>
    import { hostStore } from '$lib/stores';
    import { goto } from '$app/navigation';

    let username = 'user' + Math.floor(Math.random() * 10000);
    let email = '';
    let password = '';
    let password1 = '';
    let specialChars =/[`!#$%^&*()\+=\[\]{};':"\\|,<>\/?~ ]/

    async function signup() {

        if (password != password1) {
            alert('Passwords not matching');
        } else if (password.length < 8 || password.length > 30) {
            alert('Password too short/long');
        } else if (username.length < 4 || username.length > 50) {
            alert('Username too short/long');
        } else if (specialChars.test(username)) {
            alert("Username can't contain special characters or spaces");
        } else if (email.length < 6 || !/@/.test(email) || !/./.test(email) || specialChars.test(email) || email.length > 50) {
            alert("Incorrect Email");
        } else {
            const response = await fetch($hostStore + '/auth/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ email, username, password }),
            });

            const data = await response.json();
            if (response.ok) {
                alert('Signup successful');
                goto('/');
            } else {
                alert('Signup failed: ' + data.error);
            }
        }    

    }
</script>

<input type="email" bind:value={email} placeholder="Email">
<input type="text" bind:value={username} placeholder="Username">
<input type="password" bind:value={password} placeholder="Password">
<input type="password" bind:value={password1} placeholder="Retype password">
<button on:click={signup}>Sign Up</button>