<script>
    import { hostStore } from '$lib/stores';
    import { goto } from '$app/navigation';

    let email = '';
    let password = '';

    async function login() {
    const response = await fetch($hostStore + '/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',  // Include cookies
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();
    if (response.ok) {
      alert('Login successful');
      goto('/')
    } else {
      alert('Login failed: ' + data.error);
    }
  }

</script>

<input type="email" placeholder="E-Mail" bind:value={email}>
<input type="password" placeholder="Password" bind:value={password}>
<button on:click={login}>Log In</button>