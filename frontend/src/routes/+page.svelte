<title>Play</title>
<script>
    import { hostStore } from '$lib/stores.js';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';

    async function logout() {
        const response = await fetch($hostStore + '/auth/logout', {
            method: 'GET',
            credentials: 'include'
        });

        const data = await response.json();
        if (response.ok) {
            alert('Logged out successfully');
            goto('auth/login')
        } else {
            alert('Logout failed: ' + data.error);
        }
    }

    async function getUser() {
        const user_info = await fetch($hostStore + '/auth/user', {
            method: 'GET',
            credentials: 'include'
        });

        if (user_info.ok) {
            alert('Continiue');
        } else {
            alert('Log in');
            goto('auth/login')
        }
    }

    onMount(() => {
        getUser();
    });


</script>

<audio controls>
    <source src="{$hostStore}/index">
</audio>
<button on:click={logout}>Log Out</button>
