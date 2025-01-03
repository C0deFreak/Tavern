<script>
    import { goto, hostStore } from '$lib/libraries'

    let name = 'user' + Math.floor(Math.random() * 10000);
    let email = '';
    let password = '';
    let password1 = '';
    let specialChars =/[`!#$%^&*()\+=\[\]{};':"\\|,<>\/?~ ]/

    async function signup() {

        if (password != password1) {
            goto('/auth/sign-up');
        } else if (password.length < 8 || password.length > 30) {
            goto('/auth/sign-up');
        } else if (name.length < 4 || name.length > 50) {
            goto('/auth/sign-up');
        } else if (specialChars.test(name)) {
            goto('/auth/sign-up');
        } else if (email.length < 6 || !/@/.test(email) || !/./.test(email) || specialChars.test(email) || email.length > 50) {
            goto('/auth/sign-up');
        } else {
            const response = await fetch($hostStore + '/auth/signup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ email, name, password }),
            });

            if (response.ok) {
                goto('/');
                
            } else {
                goto('/auth/sign-up');
            }
        }    

    }
</script>

<input type="email" bind:value={email} placeholder="Email">
<input type="text" bind:value={name} placeholder="Username">
<input type="password" bind:value={password} placeholder="Password">
<input type="password" bind:value={password1} placeholder="Retype password">
<button on:click={signup}>Sign Up</button>