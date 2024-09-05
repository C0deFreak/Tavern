<script>
    import { hostStore } from '$lib/stores';

    let username = 'user' + Math.floor(Math.random() * 10000);
    let email = '';
    let password = '';
    let password1 = '';
    let message = 'Signing in'

    async function signUp() {
        if (password == password1) {
            const formData = new FormData();
            formData.append('username', username);
            formData.append('email', email);
            formData.append('password', password);

            await fetch($hostStore + '/auth/sign-up', {
                method: 'POST',
                body: formData,
            });
        } else {
            message = 'Passwords do not match'
        }
        
        
    }

</script>

<h1>{message}</h1>

<input type="text" placeholder="Username"  bind:value={username}>
<input type="email" placeholder="E-Mail" bind:value={email}>
<input type="password" placeholder="Password" bind:value={password}>
<input type="password" placeholder="Retype Password" bind:value={password1}>
<button on:click={signUp}>Sign Up</button>