<script>
    import { hostStore } from '$lib/stores';
    import { goto } from '$app/navigation';

    let username = 'user' + Math.floor(Math.random() * 10000);
    let email = '';
    let password = '';
    let password1 = '';
    let message = 'Signing in'

    async function signup() {
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
</script>

<input type="email" bind:value={email} placeholder="Email">
<input type="text" bind:value={username} placeholder="Username">
<input type="password" bind:value={password} placeholder="Password">
<button on:click={signup}>Sign Up</button>