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

<div class="w-full h-1/2 fixed top-0 left-0 -z-10 mt-16 ml-49 rounded-2xl px-6 py-16" style="background: linear-gradient(to bottom, darkolivegreen, #171717);">
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="email" bind:value={email} placeholder="Email">
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" bind:value={name} placeholder="Username">
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="password" bind:value={password} placeholder="Password">
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="password" bind:value={password1} placeholder="Retype password">
    <button class="px-4 py-2 bg-green-500 rounded-2xl text-xs" on:click={signup}>Sign Up</button>
</div>