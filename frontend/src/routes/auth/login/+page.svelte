<script>
    import { hostStore } from '$lib/stores';

    let email = '';
    let password = '';

    async function logIn() {
        const formData = new FormData();
        formData.append('email', email);
        formData.append('password', password)

        await fetch($hostStore + '/auth/login', {
            method: 'POST',
            body: formData,
        });
    }

</script>

<input type="email" placeholder="E-Mail" bind:value={email}>
<input type="password" placeholder="Password" bind:value={password}>
<button on:click={logIn}>Log In</button>