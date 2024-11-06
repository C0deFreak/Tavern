<script>
  import { goto, hostStore } from '$lib/libraries'

  let email = '';
  let password = '';

  async function login() {
    const response = await fetch($hostStore + '/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
      goto('/')
      location.reload()
    } else {
      goto('/auth/login');
    }
  }

</script>

<input type="email" placeholder="E-Mail" bind:value={email}>
<input type="password" placeholder="Password" bind:value={password}>
<button on:click={login}>Log In</button>